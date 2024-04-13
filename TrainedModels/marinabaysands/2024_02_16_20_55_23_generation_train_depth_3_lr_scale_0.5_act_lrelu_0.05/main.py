import datetime
import dateutil.tz
import os
import os.path as osp
from shutil import copyfile, copytree
import glob
import time
import random
import torch
import math
import argparse
from SoloSynthGAN import functions


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--not_cuda', action='store_true', help='disables cuda', default=0)
    parser.add_argument('--manualSeed', type=int, help='manual seed')


    parser.add_argument('--nfc', type=int,help='number of filters per conv layer', default=64)
    parser.add_argument('--ker_size',type=int,help='kernel size',default=3)
    parser.add_argument('--num_layer',type=int,help='number of layers per stage',default=3)
    parser.add_argument('--padd_size',type=int,help='net pad size',default=0)
        
 
    parser.add_argument('--nc_im',type=int,help='image # channels',default=3)
    parser.add_argument('--noise_amp',type=float,help='additive noise cont weight',default=0.1)
    parser.add_argument('--min_size',type=int,help='image minimal size at the coarser scale',default=25)
    parser.add_argument('--max_size', type=int,help='image minimal size at the coarser scale', default=250)
    parser.add_argument('--train_depth', type=int, help='how many layers are trained if growing', default=3)
    parser.add_argument('--start_scale', type=int, help='at which stage to start training', default=0)

  
    parser.add_argument('--niter', type=int, default=1500, help='number of epochs to train per scale')
    parser.add_argument('--gamma',type=float,help='scheduler gamma',default=0.1)
    parser.add_argument('--lr_g', type=float, default=0.0005, help='learning rate, default=0.0005')
    parser.add_argument('--lr_d', type=float, default=0.0005, help='learning rate, default=0.0005')
    parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
    parser.add_argument('--Gsteps',type=int, help='Generator inner steps',default=3)
    parser.add_argument('--Dsteps',type=int, help='Discriminator inner steps',default=3)
    parser.add_argument('--lambda_grad',type=float, help='gradient penalty weight',default=0.1)
    parser.add_argument('--alpha',type=float, help='reconstruction loss weight',default=10)
    parser.add_argument('--activation', default='lrelu', help="activation function {lrelu, prelu, elu, selu}")
    parser.add_argument('--lrelu_alpha', type=float, help='alpha for leaky relu', default=0.05)
    parser.add_argument('--batch_norm', action='store_true', help='use batch norm in generator', default=0)

    return parser




if __name__ == '__main__':
    parser = get_arguments()
    parser.add_argument('--input_name', help='input image name for training', required=True)
    parser.add_argument('--naive_img', help='naive input image  (harmonization or editing)', default="")
    parser.add_argument('--gpu', type=int, help='which GPU to use', default=0)
    parser.add_argument('--train_mode', default='generation',
                        choices=['generation', 'retarget', 'harmonization', 'editing', 'animation'],
                        help="generation, retarget, harmonization, editing, animation")
    parser.add_argument('--lr_scale', type=float, help='scaling of learning rate for lower stages', default=0.5)
    parser.add_argument('--train_stages', type=int, help='how many stages to use for training', default=6)

    parser.add_argument('--fine_tune', action='store_true', help='whether to fine tune on a given image', default=0)
    parser.add_argument('--model_dir', help='model to be used for fine tuning (harmonization or editing)', default="")

    opt = parser.parse_args()
    print(opt)
    opt = functions.post_config(opt)
    

    if opt.fine_tune:
        _gpu = opt.gpu
        _model_dir = opt.model_dir
        _timestamp = opt.timestamp
        _naive_img = opt.naive_img
        _niter = opt.niter

        opt = functions.load_config(opt)

        opt.gpu = _gpu
        opt.model_dir = _model_dir
        opt.start_scale = opt.train_stages - 1
        opt.timestamp = _timestamp
        opt.fine_tune = True
        opt.naive_img = _naive_img
        opt.niter = _niter

    if not os.path.exists(opt.input_name):
        print("Image does not exist: {}".format(opt.input_name))
        print("Please specify a valid image.")
        exit()

    if torch.cuda.is_available():
        torch.cuda.set_device(opt.gpu)


    if opt.train_mode == "generation" or opt.train_mode == "retarget" or opt.train_mode == "animation":
        if opt.train_mode == "animation":
            opt.min_size = 20
        from SoloSynthGAN.training_generation import *

    dir2save = functions.generate_dir2save(opt)

    if osp.exists(dir2save):
        print('Trained model already exist: {}'.format(dir2save))
        exit()
    try:
        os.makedirs(dir2save)
    except OSError:
        pass

    with open(osp.join(dir2save, 'parameters.txt'), 'w') as f:
        for o in opt.__dict__:
            f.write("{}\t-\t{}\n".format(o, opt.__dict__[o]))
    current_path = os.path.dirname(os.path.abspath(__file__))
    for py_file in glob.glob(osp.join(current_path, "*.py")):
        copyfile(py_file, osp.join(dir2save, py_file.split("/")[-1]))
    copytree(osp.join(current_path, "SoloSynthGAN"), osp.join(dir2save, "SoloSynthGAN"))



    print("Training model ({})".format(dir2save))
    start = time.time()
    train(opt)
    end = time.time()
    elapsed_time = end - start
    print("Time for training: {} seconds".format(elapsed_time))
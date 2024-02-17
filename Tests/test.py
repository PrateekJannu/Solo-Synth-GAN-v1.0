import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))


parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)





from SoloSynthGAN import functions
from test_functions import *
import unittest

from argparse import Namespace
opt=Namespace(Dsteps=3, Gsteps=3, activation='lrelu', alpha=10, batch_norm=0, beta1=0.5, fine_tune=0, gamma=0.1, gpu=0, input_name='Images/marinabaysands.jpg', ker_size=3, lambda_grad=0.1, lr_d=0.0005, lr_g=0.0005, lr_scale=0.5, lrelu_alpha=0.05, manualSeed=None, max_size=250, min_size=25, model_dir='', naive_img='', nc_im=3, nfc=64, niter=1500, noise_amp=0.1, not_cuda=1, num_layer=3, padd_size=0, start_scale=0, train_depth=3, train_mode='generation', train_stages=6)
def denorm_tester(x):
    out = (x + 1) / 2
    return out.clamp(0, 1)




def norm_tester(x):
    out = (x - 0.5) * 2
    return out.clamp(-1, 1)


def convert_image_np_tester(inp):
    if inp.shape[1]==3:
        inp = denorm_tester(inp)
        inp = move_to_cpu(inp[-1,:,:,:])
        inp = inp.numpy().transpose((1,2,0))
    else:
        inp = denorm_tester(inp)
        inp = move_to_cpu(inp[-1,-1,:,:])
        inp = inp.numpy().transpose((0,1))

    inp = np.clip(inp,0,1)
    return inp


def generate_noise(size,num_samp=1,device='cuda',type='gaussian', scale=1):
    if type == 'gaussian':
        noise = torch.randn(num_samp, size[0], round(size[1]/scale), round(size[2]/scale), device=device)
        noise = upsampling(noise,size[1], size[2])
    elif type =='gaussian_mixture':
        noise1 = torch.randn(num_samp, size[0], size[1], size[2], device=device)+5
        noise2 = torch.randn(num_samp, size[0], size[1], size[2], device=device)
        noise = noise1+noise2
    elif type == 'uniform':
        noise = torch.randn(num_samp, size[0], size[1], size[2], device=device)
    else:
        raise NotImplementedError
    return noise


def upsampling(im,sx,sy):
    m = nn.Upsample(size=[round(sx),round(sy)],mode='bilinear',align_corners=True)
    return m(im)


def move_to_gpu(t):
    if (torch.cuda.is_available()):
        t = t.to(torch.device('cuda'))
    return t


def move_to_cpu(t):
    t = t.to(torch.device('cpu'))
    return t


def save_image(name, image):
    plt.imsave(name, convert_image_np_tester(image), vmin=0, vmax=1)


def sample_random_noise(depth, reals_shapes, opt):
    noise = []
    for d in range(depth + 1):
        if d == 0:
            noise.append(generate_noise([opt.nc_im, reals_shapes[d][2], reals_shapes[d][3]],
                                         device=opt.device).detach())
        else:
            if opt.train_mode == "generation" or opt.train_mode == "animation":
                noise.append(generate_noise([opt.nfc, reals_shapes[d][2] + opt.num_layer * 2,
                                             reals_shapes[d][3] + opt.num_layer * 2],
                                             device=opt.device).detach())
            else:
                noise.append(generate_noise([opt.nfc, reals_shapes[d][2], reals_shapes[d][3]],
                                             device=opt.device).detach())

    return noise

def calc_gradient_penalty_tester(netD, real_data, fake_data, LAMBDA, device):
    MSGGan = False
    if  MSGGan:
        alpha = torch.rand(1, 1)
        alpha = alpha.to(device)  # cuda() #gpu) #if use_cuda else alpha

        interpolates = [alpha * rd + ((1 - alpha) * fd) for rd, fd in zip(real_data, fake_data)]
        interpolates = [i.to(device) for i in interpolates]
        interpolates = [torch.autograd.Variable(i, requires_grad=True) for i in interpolates]

        disc_interpolates = netD(interpolates)
    else:
        alpha = torch.rand(1, 1)
        alpha = alpha.expand(real_data.size())
        alpha = alpha.to(device)  # cuda() #gpu) #if use_cuda else alpha

        interpolates = alpha * real_data + ((1 - alpha) * fake_data)
        interpolates = interpolates.to(device)#.cuda()
        interpolates = torch.autograd.Variable(interpolates, requires_grad=True)

        disc_interpolates = netD(interpolates)

    gradients = torch.autograd.grad(outputs=disc_interpolates, inputs=interpolates,
                              grad_outputs=torch.ones(disc_interpolates.size()).to(device),#.cuda(), #if use_cuda else torch.ones(
                                  #disc_interpolates.size()),
                              create_graph=True, retain_graph=True, only_inputs=True)[0]
    #LAMBDA = 1
    gradient_penalty = ((gradients.norm_tester(2, dim=1) - 1) ** 2).mean() * LAMBDA
    return gradient_penalty
class Tests(unittest.TestCase):


    def test_norm(self):
        for i in range(100000):
            b=torch.rand(1)
            self.assertEqual(functions.norm(b),norm_tester(b)) 
            pass

    def test_np2torch(self):
        for i in range(100000):
            b=np.random.rand(8,8,8)
            self.assertEqual(torch.equal(functions.np2torch(b,opt),np2torch_tester(b,opt)),1) 
            pass
    def test_torch_to_int(self):
        for i in range(100000):
            b=torch.rand(8,8,8,8)
            self.assertEqual(np.all(functions.torch2uint8(b)==torch2uint8_tester(b)),1) 
            pass

    def test_denorm(self):
        for i in range(100000):
            b=torch.rand(1)
            self.assertEqual(functions.denorm(b),denorm_tester(b)) 
            pass


    def test_image_np(self):
        for i in range(100000):
            b=torch.rand(4,4,4,4)
            self.assertTrue(np.all(functions.convert_image_np(b)==convert_image_np_tester(b))) 
            pass



if __name__=="__main__":
    unittest.main()
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))


parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)





from SoloSynthGAN import functions
from test_functions import *
import unittest

from argparse import Namespace
opt=Namespace(Dsteps=3, Gsteps=3, activation='lrelu', alpha=10, batch_norm=0, beta1=0.5, fine_tune=0, gamma=0.1, gpu=0, input_name='Images/marinabaysands.jpg', ker_size=3, lambda_grad=0.1, lr_d=0.0005, lr_g=0.0005, lr_scale=0.5, lrelu_alpha=0.05, manualSeed=None, max_size=250, min_size=25, model_dir='', naive_img='', nc_im=3, nfc=64, niter=1500, noise_amp=0.1, not_cuda=0, num_layer=3, padd_size=0, start_scale=0, train_depth=3, train_mode='generation', train_stages=6)

class Tests(unittest.TestCase):


    def test_norm(self):
        for i in range(100):
            b=torch.rand(1)
            self.assertEqual(functions.norm(b),norm_tester(b)) 
            pass

    def test_np2torch(self):
        for i in range(100):
            b=np.random.rand(8,8,8)
            self.assertEqual(torch.equal(functions.np2torch(b,opt),np2torch_tester(b,opt)),1) 
            pass
    def test_torch_to_int(self):
        for i in range(100):
            b=torch.rand(8,8,8,8)
            self.assertEqual(np.all(functions.torch2uint8(b)==torch2uint8_tester(b)),1) 
            pass

    def test_denorm(self):
        for i in range(100):
            b=torch.rand(1)
            self.assertEqual(functions.denorm(b),denorm_tester(b)) 
            pass


    def test_image_np(self):
        for i in range(100):
            b=torch.rand(4,4,4,4)
            self.assertTrue(np.all(functions.convert_image_np(b)==convert_image_np_tester(b))) 
            pass



if __name__=="__main__":
    unittest.main()
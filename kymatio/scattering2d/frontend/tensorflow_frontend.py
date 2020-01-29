import tensorflow as tf
from ...frontend.tensorflow_frontend import ScatteringTensorFlow
from kymatio.scattering2d.core.scattering2d import scattering2d
from .base_frontend import ScatteringBase2D

class ScatteringTensorFlow2D(ScatteringTensorFlow, ScatteringBase2D):
    def __init__(self, J, shape, L=8, max_order=2, pre_pad=False, backend='tensorflow', name='Scattering2D'):
        ScatteringTensorFlow.__init__(self, name)
        ScatteringBase2D.__init__(self, J, shape, L, max_order, pre_pad, backend)
        ScatteringBase2D._instantiate_backend(self, 'kymatio.scattering2d.backend.')
        ScatteringBase2D.build(self)
        ScatteringBase2D.create_filters(self)

    def scattering(self, input):
        with tf.name_scope('scattering') as scope:
            try:
                input = tf.convert_to_tensor(input)
            except ValueError:
                raise TypeError('The input should be convertible to a '
                                'TensorFlow Tensor.')

            if len(input.shape) < 2:
                raise RuntimeError('Input tensor should have at least two '
                                   'dimensions.')

            if (input.shape[-1] != self.N or input.shape[-2] != self.M) and not self.pre_pad:
                raise RuntimeError('Tensor must be of spatial size (%i,%i).' % (self.M, self.N))

            if (input.shape[-1] != self.N_padded or input.shape[-2] != self.M_padded) and self.pre_pad:
                raise RuntimeError('Padded tensor must be of spatial size (%i,%i).' % (self.M_padded, self.N_padded))

            batch_shape = tuple(input.shape[:-2])
            signal_shape = tuple(input.shape[-2:])

            input = tf.reshape(input, (-1,) + signal_shape)

            S = scattering2d(input, self.pad, self.unpad, self.backend, self.J, self.L, self.phi, self.psi,
                             self.max_order, vectorize=self.vectorize)
            scattering_shape = tuple(S.shape[-3:])
            S = tf.reshape(S, batch_shape + scattering_shape)
            return S


__all__ = ['ScatteringTensorFlow2D']

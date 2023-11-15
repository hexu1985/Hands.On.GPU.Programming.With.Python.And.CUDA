import pycuda
import pycuda.driver as drv
drv.init()

print 'CUDA device query (PyCUDA version) \n'

print 'Detected {} CUDA Capable device(s) \n'.format(drv.Device.count())

for i in range(drv.Device.count()):
    
    gpu_device = drv.Device(i)
    print 'Device {}: {}'.format( i, gpu_device.name() ) 
    compute_capability = float( '%d.%d' % gpu_device.compute_capability() )
    print '\t Compute Capability: {}'.format(compute_capability)
    print '\t Total Memory: {} megabytes'.format(gpu_device.total_memory()//(1024**2))
    
    # The following will give us all remaining device attributes as seen 
    # in the original deviceQuery.
    # We set up a dictionary as such so that we can easily index
    # the values using a string descriptor.
    
    device_attributes_tuples = gpu_device.get_attributes().iteritems() 
    device_attributes = {}
    
    for k, v in device_attributes_tuples:
        device_attributes[str(k)] = v
    
    num_mp = device_attributes['MULTIPROCESSOR_COUNT']
    
    # Cores per multiprocessor is not reported by the GPU!  
    # We must use a lookup table based on compute capability.
    # See the following:
    # http://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#compute-capabilities
    # https://en.wikipedia.org/wiki/CUDA#References
    # after 7.0: 64 cores per mp 
    cuda_cores_per_mp = { 
            1.0 : 8, 1.1 : 8, 1.2 : 8, 1.3 : 8,
            2.0 : 32, 2.1 : 48, 
            3.0 : 192, 3.2 : 192, 3.5 : 192, 3.7 : 192, 
            5.0 : 128, 5.2 : 128, 5.3 : 128, 
            6.0 : 64, 6.1 : 128, 6.2 : 128,
            }.get(compute_capability, 64)
    
    print '\t ({}) Multiprocessors, ({}) CUDA Cores / Multiprocessor: {} CUDA Cores'.format(num_mp, cuda_cores_per_mp, num_mp*cuda_cores_per_mp)
    
    device_attributes.pop('MULTIPROCESSOR_COUNT')
    
    for k in device_attributes.keys():
        print '\t {}: {}'.format(k, device_attributes[k])

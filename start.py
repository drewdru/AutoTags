import sys, os
import neural_network.main as neural_network
import vk_base.main as vk_base

def network():
    print('test')
    neural_network.main()

def vk_db():
    vk_base.main()

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        if sys.argv[1] == 'network':
            print('test')
            network()
        elif sys.argv[1] == 'vk_db':
            vk_db()

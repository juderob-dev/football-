import skimage                 # form 1, load whole skimage library
import skimage.io              # form 2, load skimage.io module only
from skimage.io import imread  # form 3, load only the imread function
import numpy as np
def readImage():
    image = skimage.io.imread(fname="data/eight.tif")
    plt.imshow(image)

if __name__=="__main__":
    print(solution([1,2,4,8]))
    print(skimage.__version__)
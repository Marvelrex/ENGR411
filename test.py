import ShannonCode
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
import collections

img = data.chelsea()
height = img.shape[0]
width = img.shape[1]
# Count frequency of each point R+G+B/3
count = collections.Counter(list(img.flatten()))
# Get the set of counts
color = list(count.keys())
# Calculate frequency of each point
number = list(count.values())
number = np.array(number)

# Calculate probability
p = number / np.sum(number)

shannon = ShannonCode.ShannonCoding(color, p)

# Encode image and save to a txt file
total_code = shannon.encode(img)

# Get height and width


# Grayscale in coding form
a = shannon.decode(total_code)
# Reshape to orignal shape
a = a.reshape(height, width,3)

shannon.print_format()

plt.subplot(121)
plt.title('Original')
plt.imshow(img)
plt.imsave("Original.png",img)
plt.subplot(122)
plt.title('After Coding')
plt.imshow(a)
plt.imsave("AfterCoding.png",a)
plt.show()

import torch
import clip
from PIL import Image
from sklearn.cluster import KMeans
import imageio

num_of_frame = 34
device = "cuda" if torch.cuda.is_available() else "cpu"

def extractor(img_path, model, preprocess):
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features.cpu().data.numpy()[0]


def choose_frame(c, max_frame):
    res = []
    for i in range(4):
        if c[i] < 7:
            res = res + [c[i], c[i] + 1 , c[i] + 2, c[i] + 3, c[i] + 4, c[i] + 5, c[i] + 6]
        elif c[i] > max_frame - 7:
            res = res + [c[i], c[i] - 1 , c[i] - 2, c[i] - 3, c[i] - 4, c[i] - 5, c[i] - 6]
        else:
            res = res + [c[i], c[i] - 1 , c[i] - 2, c[i] - 3, c[i] + 1 , c[i] + 2, c[i] + 3]
    res.sort()
    return res

if __name__ == '__main__':
    model, preprocess = clip.load("ViT-B/32", device=device)
    featurelist = []
    for i in range(num_of_frame):
        image_name = "pic-" + str(i) + ".jpg"
        image_path = "./pic/" + image_name
        image_feature = extractor(image_path, model, preprocess)
        featurelist.append(image_feature)     
    
    kmeans = KMeans(n_clusters=4, max_iter=300).fit_transform(featurelist)

    c = [0, 0, 0, 0]
    d = [1000.0, 1000.0, 1000.0, 1000.0]

    for i in range(num_of_frame):
        k = kmeans[i]
        for j in range(4):
            if k[j] < d[j]:
                d[j] = k[j]
                c[j] = i

    frames = []
    j = choose_frame(c, num_of_frame)
    for k in range(len(j)):
        image_name = "./pic/pic-" + str(j[k]) + ".jpg"
        frames.append(imageio.imread(image_name))
        
    imageio.mimsave("test.gif", frames, 'GIF', duration=0.2)

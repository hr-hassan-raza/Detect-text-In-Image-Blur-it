from easyocr import Reader
import argparse
import cv2
import os

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

## Function to check if point lies in rectangle 
def FindPoint(x1, y1, x2,
              y2, x, y) :
    if (x > x1 and x < x2 and
        y > y1 and y < y2) :
        return True
    else :
        return False


def click_event(event, x, y, flags, params):
    # checking for right mouse clicks    
    if event==cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        for i in range(len(top)):
            a = FindPoint(top[i][0], top[i][1], bottom[i][0],
              bottom[i][1], x, y)
            if (a):
                topLeft = top[i]
                bottomRight = bottom[i]
                x, y = topLeft[0], topLeft[1]
                w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]
                # Grab ROI with Numpy slicing and blur
                ROI = image[y:y+h, x:x+w]
                blur = cv2.GaussianBlur(ROI, (51,51), 0) 
                # Insert ROI back into image
                image[y:y+h, x:x+w] = blur
                cv2.imshow('image', image)
        path = os.getcwd()+ '/result' + args['image'][6:]
        cv2.imwrite(path,image)
        
if __name__ == "__main__" :
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image to be OCR'd")
    ap.add_argument("-l", "--langs", type=str, default="en",
        help="comma separated list of languages to OCR")
    ap.add_argument("-g", "--gpu", type=int, default=-1,
        help="whether or not GPU should be used")
    args = vars(ap.parse_args())

    # break the input languages into a comma separated list
    langs = args["langs"].split(",")
    print("[INFO] OCR'ing with the following languages: {}".format(langs))
    # load the input image from disk
    image = cv2.imread(args["image"])
    # OCR the input image using EasyOCR
    print("[INFO] OCR'ing input image...")
    reader = Reader(langs, gpu=args["gpu"] > 0)
    results = reader.readtext(image)
    top = []
    bottom = []
    # loop over the results
    for (bbox, text, prob) in results:
        # display the OCR'd text and associated probability
        print("[INFO] {:.4f}: {}".format(prob, text))
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        # cleanup the text and draw the box surrounding the text along
        # with the OCR'd text itself
        text = cleanup_text(text)
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        top.append(tl)
        bottom.append(br)
    # show the output image
    cv2.imshow('image', image)
    # setting mouse hadler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()
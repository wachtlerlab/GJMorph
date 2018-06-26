"""
Description:        This file contains functions for combining three images of an object taken from three orthogonal
                    views into a single image

Usage:              python processOrthoProjBlender.py <baseNameOfImages> <real size of dummy cube>

Note:               The input images are to be saved as "<baseNameOfImages>XY.png", "<baseNameOfImages>XZ.png" and
                    "<baseNameOfImages>YZ.png". The scene of which the three views are obtained must also contain a
                    cube of surface color with RGBA [0.459, 0.459, 0.478, 1]. This cube along with it's real size
                    supplied as argument is used to calculate the scale of the scene and add scale bars. The script
                    expects the background color of the scene to have RGBA [0.224, 0.224, 0.224, 1] which is the
                    default background color of Blender. This background color will be replaced by
                    [0.918, 0.918, 0.949, 1]

Warning:            Will consume **A LOT OF RAM** when running as the three images as well as the result images are
                    created.
"""

import os
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.ndimage import rotate, label, find_objects, binary_dilation
import GJMorph
GJEMSETC = os.path.join(GJMorph.__path__[0], 'etc')
import sys


def getSquareSide(imIn, squareColor, replaceColor):
    '''
    Calculates the size of the square of color <squareColor> in pixels.
    :param imIn: 3 dimensional ndarray, input image
    :param squareColor: 3 float iterable, RGB of square
    :param replaceColor: 3 float iterable, RGB of the color with which all pixels of square will be replaced
    :return: 3 dimensional ndarray, image with all pixels of the square is replaced with <replaceColor>
    '''

    colorMask = np.logical_and(imIn[:, :, 0] == squareColor[0],
                               imIn[:, :, 1] == squareColor[1],
                               imIn[:, :, 2] == squareColor[2])
    ccLabelImg, nLabels = label(colorMask)

    ccLabels = []
    ccVolumes = []
    for ccLabel in range(1, nLabels + 1):
        ccLabels.append(ccLabel)
        ccVolumes.append((ccLabelImg == ccLabel).sum())

    largestVolume = max(ccVolumes)
    squareSide = largestVolume ** 0.5

    largestCCLabel = ccLabels[int(np.argmax(ccVolumes))]

    largestCCMask = ccLabelImg == largestCCLabel
    largestCCMaskDialated = binary_dilation(largestCCMask, np.ones((5, 5)))

    outImg = imIn.copy()
    outImg[largestCCMaskDialated] = replaceColor

    return squareSide, outImg





def addSmallAxes(imIn, texts, position, scalePixelPerUm, maxExtent=None):
    """
    Adds a pair of small perpendicular axes with labels and scale at the position specified by <position>
    :param imIn: 3-dimensional ndarray, input image
    :param texts: 2 member tuple of strings, labels to use for horizontal and vertical axes
    :param position: string, one of "br", "bl", "tr", "tl" meaning "bottom right", "bottom left", "top right" and
    "top left" respectively.
    :param scalePixelPerUm: float, scale of image in pixel per micrometer
    :param maxExtent: 2 member tuple of floats, can be used to overide the internal estimation of image size that is
    used for margin calcualions
    :return: 3-dimensional ndarray, output image with axes
    """

    if type(imIn) is str and os.path.isfile(imIn):
        im = Image.open(imIn)
    elif type(imIn) is np.ndarray:
        assert len(imIn.shape) == 3 and imIn.shape[2] in (1, 3, 4), 'Improper format for input ndarray imIn'
        if imIn.dtype != 'uint8':
            dMax = np.max(imIn)
            dMin = np.min(imIn)
            imIn = np.array(255 * (imIn  - dMin) / (dMax - dMin), dtype='uint8')
        im = Image.fromarray(imIn)
        im.readonly = 0
    else:
        raise (TypeError('imIn'))

    draw = ImageDraw.Draw(im)

    marginFraction = 0.075
    lineLengthFraction = 0.175

    xlim = [0, im.size[0]]
    ylim = [0, im.size[1]]

    if maxExtent is None:
        maxExtent = float(max(ylim[1] - ylim[0], xlim[1] - xlim[0]))

    fontsize = int(150 * maxExtent / 3000.0)
    lw = int(8 * maxExtent / 3000.0)

    margin = marginFraction * maxExtent
    approxLineLength = lineLengthFraction * maxExtent

    lineLengthInUm = approxLineLength / scalePixelPerUm
    possibleCandidates = np.array([10, 20, 100, 150, 500, 1000])
    tempDists = possibleCandidates - lineLengthInUm
    tempDistsAbs = np.abs(tempDists)

    lineLengthInUmAdjusted = possibleCandidates[tempDistsAbs.argmin()]

    lineLength = lineLengthInUmAdjusted * scalePixelPerUm

    if position == 'br':
        arrowYs = [ylim[1] - margin, ylim[1] - (margin + lineLength)]
        arrowXs = [xlim[1] - (margin + lineLength), xlim[1] - margin]
    elif position == 'bl':
        arrowYs = [ylim[1] - margin, ylim[1] - (margin + lineLength)]
        arrowXs = [xlim[0] + margin, xlim[0] + (margin + lineLength)]
    elif position == 'tl':
        arrowYs = [ylim[0] + (margin + lineLength), ylim[0] + margin]
        arrowXs = [xlim[0] + margin, xlim[0] + (margin + lineLength)]
    elif position == 'tr':
        arrowYs = [ylim[0] + (margin + lineLength), ylim[0] + margin]
        arrowXs = [xlim[1] - (margin + lineLength), xlim[1] - margin]
    else:
        raise(ValueError('Argument position must be one of \'bl\', \'br\', \'tl\' or \'tr\''))

    draw.line((arrowXs[0], arrowYs[0], arrowXs[1], arrowYs[0]), fill='rgb(0, 0, 0)', width=lw)
    draw.line((arrowXs[0], arrowYs[0], arrowXs[0], arrowYs[1]), fill='rgb(0, 0, 0)', width=lw)

    font = ImageFont.truetype(os.path.join(GJEMSETC, 'FreeSans.ttf'), fontsize)
    # draw.text((arrowXs[0] - 0.5 * margin,
    #            0.5 * (arrowYs[1] + arrowYs[0]) - 0.1 * margin),
    #           "{:2d} um".format(lineLengthInUmAdjusted), fill='rgb(255, 255, 255)', font=font,
    #           )
    draw.text((arrowXs[0] - 0.2 * margin,
               arrowYs[0] + 0.1 * margin),
              "{:2d} um".format(lineLengthInUmAdjusted), fill='rgb(0, 0, 0)',
              font=font)
    draw.text((arrowXs[0] + 0.15 * margin,
               arrowYs[1] - 0.5 * margin),
              texts[1], fill='rgb(0, 0, 0)', font=font)
    draw.text((arrowXs[1] + 0.15 * margin,
               arrowYs[0] - 0.6 * margin),
              texts[0], fill='rgb(0, 0, 0)', font=font)

    return np.asarray(im) / 255.0


def cropImage(imIn, bgColor, bgColor2Rep=None, extents=(None, None)):
    """
    Crops an image according to limits in <extents> and replaces all pixels with <bgColor2Rep> with <bgColor>
    :param imIn: 3-dimensional ndarray, input image
    :param bgColor: 4 member float iterable, RGBA of a color
    :param bgColor2Rep: 4 member float iterable, RGBA of a color
    :param extents: 2 member tuple of floats, can be used to override internally calculated extent of the object along
    X and Y axes, using bounding box.
    :return: 3-dimensional ndarray, output image cropped and BG color replaced
    """

    if type(imIn) is str and os.path.isfile(imIn):
        im = np.around(plt.imread(imIn), 3)
    elif type(imIn) is np.ndarray:
        assert len(imIn.shape) == 3 and imIn.shape[2] in (1, 3, 4), 'Improper format for input ndarray imIn'
        im = imIn
    else:
        raise (TypeError('imIn'))

    if bgColor:
        assert len(bgColor) == im.shape[2], 'The color representation of bgColor is not consistent with imIn'
    if bgColor2Rep:
        assert len(bgColor) == im.shape[2], 'The color representation of bgColor is not consistent with imIn'

    colorMatches = [im[:, :, x] == bgColor[x] for x in range(im.shape[2])]
    bgImage = reduce(np.logical_and, colorMatches)
    fgImage = np.logical_not(bgImage)
    fgInds = np.where(fgImage)
    if bgColor2Rep:
        im[bgImage] = bgColor2Rep

    if extents[0]:
        xExtent = extents[0]
    else:
        xExtent = int(100 * np.ceil((max(fgInds[0]) - min(fgInds[0])) / 100.0))
    xCenter = (max(fgInds[0]) + min(fgInds[0])) / 2
    if extents[1]:
        yExtent = extents[1]
    else:
        yExtent = int(100 * np.ceil((max(fgInds[1]) - min(fgInds[1])) / 100.0))
    yCenter = (max(fgInds[1]) + min(fgInds[1])) / 2
    imOut = np.empty((xExtent, yExtent, im.shape[2]))
    for ind in range(imOut.shape[2]):
        imOut[:, :, ind] = bgColor2Rep[ind]

    xBounds = [max(0, xCenter - xExtent / 2), min(xCenter + xExtent / 2, im.shape[0])]
    yBounds = [max(0, yCenter - yExtent / 2), min(yCenter + yExtent / 2, im.shape[1])]

    xBoundsOut = [(xExtent / 2) - (xCenter - xBounds[0]), (xExtent / 2) + (xBounds[1] - xCenter)]
    yBoundsOut = [(yExtent / 2) - (yCenter - yBounds[0]), (yExtent / 2) + (yBounds[1] - yCenter)]

    # print xBounds
    # print yBounds
    # print xBoundsOut
    # print yBoundsOut

    imOut[xBoundsOut[0]: xBoundsOut[1], yBoundsOut[0]: yBoundsOut[1], :] = \
        im[xBounds[0]: xBounds[1], yBounds[0]: yBounds[1], :]

    return imOut


def addImageMargin(imIn, bgColor=None, margin=0):
    """
    Adds margin of <margin> pixels on all sides to an image using the background color <bgColor>
    :param imIn: 3-dimensional ndarray, input image
    :param bgColor: 4 member float iterable, representing RGBA of the background color
    :param margin: int, number of pixels to pad each side.
    :return: 3-dimensional ndarray, output image
    """

    if type(imIn) is str and os.path.isfile(imIn):
        im = np.around(plt.imread(imIn), 3)
    elif type(imIn) is np.ndarray:
        assert len(imIn.shape) == 3 and imIn.shape[2] in (1, 3, 4), 'Improper format for input ndarray imIn'
        im = imIn
    else:
        raise (TypeError('imIn'))

    if bgColor:
        assert len(bgColor) == im.shape[2], 'The color representation of bgColor is not consistent with imIn'

    imOut = np.empty((int(im.shape[0] + 2 * margin), int(im.shape[1] + 2 * margin), im.shape[2]))

    for ind in range(imOut.shape[2]):
        imOut[:, :, ind] = bgColor[ind]

    imOut[margin:-margin, margin:-margin, :] = imIn

    return imOut

if __name__ == '__main__':

    assert len(sys.argv) == 3, 'Improper Usage! Please use as:\n' \
                               'python {} <ortho projection stem> ' \
                               '<reference cube side in um>'.format(sys.argv[0])
    root = sys.argv[1]
    refCubeSideInUm = float(sys.argv[2])

    xyImage = root + 'XY.png'
    xzImage = root + 'XZ.png'
    yzImage = root + 'YZ.png'

    for x in [xyImage, xzImage, yzImage]:
        assert os.path.exists(x), 'File ' + x + 'not found'

    outFile = root + 'XYZ.png'

    axisPoss = {tuple('yx'): 'br', tuple('zx'): 'br', tuple('zy'): 'bl'}

    bgColor = [0.224, 0.224, 0.224, 1]
    replaceBGColor = [0.918, 0.918, 0.949, 1]
    refCubeColor = [0.459, 0.459, 0.478, 1]

    imageMargin = 0.22
    imageSepMargin = 0.0075

    imagesF = {}
    imagesF[tuple('yx')] = xyImage
    imagesF[tuple('zx')] = xzImage
    imagesF[tuple('zy')] = yzImage


    croppedImages = {}
    extents = {}
    scales = {} # in pixels per um
    for k, inImgFName in imagesF.iteritems():
        inImgData = plt.imread(inImgFName).round(3)
        squareSizePixels, noCubeImg = getSquareSide(inImgData, refCubeColor, replaceBGColor)
        scale = squareSizePixels / refCubeSideInUm
        scales[k] = scale
        croppedImages[k] = cropImage(noCubeImg, bgColor, replaceBGColor, [extents[a] if a in extents else None for a in k])

        for axisInd, axis in enumerate(k):
            if axis not in extents:
                extents[axis] = croppedImages[k].shape[axisInd]

    croppedMarginImages = {k: addImageMargin(v, replaceBGColor,
                                             int(imageMargin * max(extents.values())),
                                             )
                           for k, v in croppedImages.iteritems()}

    maxExtent = max(extents.values())

    croppedMAxisImages = {}
    fullExtents = {}
    for k, inImgData in croppedMarginImages.iteritems():
        croppedMAxisImages[k] = \
            addSmallAxes(inImgData,
                         [x.upper() for x in k[::-1]],
                         axisPoss[k],
                         scales[k],
                         maxExtent)

        for axisInd, axis in enumerate(k):
            if axis not in fullExtents:
                fullExtents[axis] = croppedMAxisImages[k].shape[axisInd]
        # print(fullExtents)

    # print(fullExtents)
    finalXExtent = fullExtents['y'] + fullExtents['z']
    finalYExtent = fullExtents['x'] + fullExtents['z']
    sepMargin = int(imageSepMargin * 0.5 * (finalYExtent + finalXExtent))
    finalYExtent += sepMargin
    finalXExtent += sepMargin
    finalImage = np.ones((finalXExtent, finalYExtent, 4))
    finalImage[:fullExtents['y'], :fullExtents['x'], :] = croppedMAxisImages[tuple('yx')]
    finalImage[:fullExtents['y'], -fullExtents['z']:, :] = rotate(croppedMAxisImages[tuple('zy')], 90)
    finalImage[-fullExtents['z']:, :fullExtents['x'], :] = croppedMAxisImages[tuple('zx')]

    finalImage[finalImage > 1.0] = 1.0

    finalImage[finalImage < 0] = 0

    plt.imsave(outFile, finalImage)





# Colors (B, G, R)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def transformCoordinates(coords, oldSize, newSize, newPos):
    newCoordsX = int(coords[0] * (1.0*newSize[0] / oldSize[0]) + newPos[0])
    newCoordsY = int(coords[1] * (1.0*newSize[1] / oldSize[1]) + newPos[1])
    return (newCoordsX, newCoordsY)
# end

def drawMatches(sourceImg, sCoords, targetImg, tCoords, matchList, outputMaxWidth):
    # Get new sizes of both images.  I want a 0.25 / 0.75 arrangement by width
    sOY, sOX = sourceImg.shape
    tOY, tOX = targetImg.shape
    
    sX = outputMaxWidth/4
    tX = sX * 3
    sY = int(sOY * (1.0*sX/sOX))
    tY = int(tOY * (1.0*tX/tOX))
    
    # make new blank image, size
    outputImage = np.zeros((max(sY,tY), outputMaxWidth, 3), np.uint8)
    # Scale and draw source image
    # Note that index order appears to be y,x? (row, column)
    outputImage[0:sY, 0:sX] = cv2.resize(sourceImg,(sX, sY), interpolation = cv2.INTER_AREA)[:,:,np.newaxis]
    # Scale and draw target image at offset (sX, 0)
    outputImage[0:tY, sX:sX+tX] = cv2.resize(targetImg,(tX, tY), interpolation = cv2.INTER_AREA)[:,:,np.newaxis]
    
    for m in matchList:
        # May need to tuple-ize sCoords[i], etc.
        sc = transformCoordinates(sCoords[m.queryIdx].pt, (sOX,sOY), (sX,sY), (0,0))
        tc = transformCoordinates(tCoords[m.trainIdx].pt, (tOX,tOY), (tX,tY), (sX,0))
        print sc,tc
        cv2.line(outputImage, sc, tc, WHITE, thickness=1, lineType=8, shift=0)
        # Maybe draw circles as well
        cv2.circle(outputImage, sc, 4, WHITE, thickness=1, lineType=8, shift=0)
        cv2.circle(outputImage, tc, 4, WHITE, thickness=1, lineType=8, shift=0)
        # And look into cvPutText equivalent- will be useful later
    #
    return outputImage
#

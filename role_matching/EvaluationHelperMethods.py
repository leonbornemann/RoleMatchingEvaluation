
def addFilteredBlockingMethods(df):
    df['isInStrictBlockingNoDecayWithFilter'] = ((df['isInStrictBlockingNoDecay']) & df['hasTransitionOverlapNoDecay'])
    df['isInValueSetBlockingWithFilter'] = ((df['isInValueSetBlocking']) & df['hasTransitionOverlapNoDecay'])
    df['isInSequenceBlockingWithFilter'] = ((df['isInSequenceBlocking']) & df['hasTransitionOverlapNoDecay'])
    df['isInExactMatchBlockingWithFilter'] = ((df['isInExactMatchBlocking']) & df['hasTransitionOverlapNoDecay'])

def getGroup(x):
    if(x==1.0):
        return "[1.0,1.0] (full)"
    elif(x >=0.7):
        return "[0.7,1.0) (70%)"
    else:
        return "[0.0,0.7) (<70%)"


def getWeight(bucketAndDatasetToWeight,x):
    return bucketAndDatasetToWeight[(x['dataset'],x['bucket'])]

def addDVA2VA95Blocking(df):
    df['isInDVA2VA95Blocking'] = ((df["DVACount"] >=2) & (df["VACount"]>=95))

def addParametrizedScoresAsBooleanScores(largeSampleDF):
    largeSampleDF['isIncbrbWithDecayTargetRecall95'] =  (largeSampleDF['compatibilityPercentageDecay'] >=  0.94)
    largeSampleDF['isIncbrbWithOutDecayTargetRecall95'] =  (largeSampleDF['compatibilityPercentageNoDecay'] >=  0.892241)
    largeSampleDF['isRMTargetRecall95'] = (largeSampleDF['exactSequenceMatchPercentage'] >=  0.754663)
    largeSampleDF['isSCBTargetRecall95'] = (largeSampleDF['strictlyCompatiblePercentage'] >=  0.890805)
    largeSampleDF['isSCBWithDecayTargetRecall95'] = (largeSampleDF['strictlyCompatiblePercentageWithDecay'] >=  0.93)

def addDVA2VA95Blocking(df):
    df['isInDVA2VA95Blocking'] = ((df["DVACount"] >=2) & (df["VACount"]>=95))

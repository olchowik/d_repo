'''
Created on Jun 13, 2013

@author: anna
'''
def passSubunitCondition(Mnum, Mnum_found):
    Mpass=False
    if "more" in Mnum:
        if Mnum_found>=int(Mnum.replace('_or_more','')): Mpass=True
    elif Mnum_found==int(Mnum): Mpass=True
    print Mpass
    return Mpass

def passSubunitFamCondition(Mfam, Mfam_found):
    Mpass=False
    print 'Mfam : ', Mfam
    if Mfam=='':Mpass=True
    elif Mfam in list(Mfam_found):Mpass=True
    if Mfam=='C+C1': 
        if 'C' in list(Mfam_found) or 'C1' in list(Mfam_found):Mpass=True
    #print Mfam_found
    return Mpass
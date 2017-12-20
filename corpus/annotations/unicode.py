# This Python file uses the following encoding: utf-8
import unicodedata

weird_chars = {u'\u0141': 'L', u'\u0142': 'l', u'\u00d8': 'O', u'\u00f8': 'o'}

def translateUnicodeCharByChar(text, encoding = 'ascii', joinChar = ' '): 
    """
    Translates/maps Unicode input to ascii or latin output
    deleting funny chars while retaining the base letters
    doing it char by char
    Length of return string is equal to input string
    
    """
    output = []
    for char in text:
        newchar = u''
        if weird_chars.has_key(char):
            newchar = weird_chars[char]
        else:
            try:
                newchar = char.encode(encoding)
            except UnicodeEncodeError:
                newchar = unicodedata.normalize('NFKD', char).encode(encoding, 'ignore')
        # check for length
        if len(char) != len(newchar):
        	if joinChar != None:
        		newchar = joinChar * len(char)       
        output.append(newchar)

    return u"".join(output)



def translateUnicode(text, encoding = 'ascii', joinChar = ' '):
    """
    Translates/maps Unicode input to ascii or latin output
    deleting funny chars while retaining the base letters
    Length of return string is equal to input string
    """
    if u''.__class__ == text.__class__:        
        decodedText = text
    else:
        decodedText = text.decode('utf-8', 'replace')
    newtext = u''
    try:
        newtext = decodedText.encode(encoding)
        if len(decodedText) != len(newtext):
            newtext = translateUnicodeCharByChar(decodedText, encoding, joinChar)
            print newtext
    except UnicodeEncodeError:
        newtext = translateUnicodeCharByChar(decodedText, encoding, joinChar)
    return newtext





if __name__ == '__main__':
    str = u'abcdé'
    str = u'マラリア'
    str = u'Група човешки фебрилни болести с хронично протичане, причинени от хемоспоридийни паразити от род Плазмодии, пренасяна чрез ухапване от комар Анофелес (малариен). Malaria.'
    str = u'Skupina človeških vročinskih bolezni s kroničnim ponavljanjem napadov vročine. Povzroča jo krvni parazit iz rodu plazmodijev, ki jih prenašajo komarji vrste Anopheles. (Vir: MGH)'

    newstr = translateUnicode(str)
    print len(str), len(newstr), "-"+newstr+"-"
    

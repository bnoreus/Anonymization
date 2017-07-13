# -*- coding: utf-8 -*-
import string

DL_CONFIG_PADDED_SIZE = 50

DL_CHARS = unicode(string.ascii_uppercase) + unicode(string.ascii_lowercase) + u" åäöÅÄÖ.-?!/:()\"\';_*%=+0123456789"
DL_CHARS = list(set(DL_CHARS))+["<UNK>","<PAD>","<NAME>"]
DL_CHARS = {c:i for i,c in enumerate(DL_CHARS)}
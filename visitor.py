from SmaliParser import SmaliParser
from SmaliListener import SmaliListener
import logging


def unwrap_string(word):
    return word[1:len(word) - 1]


def unwrap_init(word):
    return word[:word.index(':')]


class StringVisitor(SmaliListener):
    def __init__(self, bucket):
        self._bucket = bucket


    def registerWord(self, word):
        if word and word not in self._bucket:
            self._bucket.add(word)


    # Enter a parse tree produced by SmaliParser#sMethod.
    def enterSMethod(self, ctx:SmaliParser.SMethodContext):
        if ctx.METHOD_FULL() is not None:
            raise Exception(ctx.METHOD_FULL)

        sig = ctx.METHOD_PART().getText()
        name = sig[:sig.index("(")]
        logging.debug(f"SMethod: {name}")
        self.registerWord(name)


    # Enter a parse tree produced by SmaliParser#sField.
    def enterSField(self, ctx:SmaliParser.SFieldContext):
        v = unwrap_init(ctx.fieldObj.text)
        logging.debug("SField: {}".format(v))
        self.registerWord(v)


    # Enter a parse tree produced by SmaliParser#sParameter.
    def enterSParameter(self, ctx:SmaliParser.SParameterContext):
        v = unwrap_string(ctx.name.text)
        logging.debug(f"SParameter: {v}")
        self.registerWord(v)


    # Enter a parse tree produced by SmaliParser#sBaseValue.
    def enterSBaseValue(self, ctx:SmaliParser.SBaseValueContext):
        v = ctx.STRING()
        if v is not None:
            v = unwrap_string(v.getText())
            logging.debug(f"SBaseValue: {v}")
            self.registerWord(v)


    # Enter a parse tree produced by SmaliParser#flocal.
    def enterFlocal(self, ctx:SmaliParser.FlocalContext):
        if ctx.v2 is None:
            raise Exception("name1: {}, name2: {}, v1: {}".format(ctx.name1, ctx.name2, ctx.v1))

        name = unwrap_init(ctx.v2.text)
        name = unwrap_string(name)
        logging.debug(f"Flocal: {name}")
        self.registerWord(name)


    # Enter a parse tree produced by SmaliParser#fconst.
    def enterFconst(self, ctx:SmaliParser.FconstContext):
        if ctx.cst == SmaliParser.STRING:
            v = ctx.STRING()
            logging.debug(f"Fconst: {v}")
            self.registerWord(v)
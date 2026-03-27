import dspy
from dspy import LM

lm = LM("openai/gpt-4o")
dspy.settings.configure(lm=lm)

class DecompileSignature(dspy.Signature):
    assembly = dspy.InputField()
    code = dspy.OutputField()

class Decompiler(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(DecompileSignature)

    def forward(self, assembly):
        return self.predict(assembly=assembly)
import os
os.environ["OPENAI_API_KEY"] = "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"

import dspy
from dspy import LM

# setup model
lm = LM("openai/gpt-4o")
dspy.settings.configure(lm=lm)

# define task
class DecompileSignature(dspy.Signature):
    assembly = dspy.InputField(desc="Low-level assembly or messy decompiled code")
    code = dspy.OutputField(desc="Clean, readable C-like code")

# module
class Decompiler(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(DecompileSignature)

    def forward(self, assembly):
        return self.predict(assembly=assembly)

# test it
decompiler = Decompiler()

result = decompiler(
    assembly="""
int func(int a){
  int b;
  b = a * 2;
  return b;
}
"""
)

print(result.code)
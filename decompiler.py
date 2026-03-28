
import os
from dotenv import load_dotenv
load_dotenv()

import dspy
from dspy import LM
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
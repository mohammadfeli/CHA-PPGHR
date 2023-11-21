from __future__ import annotations
from typing import Any
from pydantic import BaseModel
from llms.llm import BaseLLM

class BaseResponseGenerator(BaseModel):
  """Base Response Generator class."""
  llm_model: BaseLLM = None
  prefix: str = ""

  class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True

  @property
  def _response_generator_type(self):
    raise "base"

  @property
  def _response_generator_model(self):
    return self.llm_model

  @property
  def _generator_prompt(self):
    return ("User: {query}\n\n"
            "Thinker:\n------------------\n{thinker}\n-------------------\n"
            "System: {prefix}. You are very helpful empathetic health assistant and your goal is to help the user to get accurate information about his/her health and well-being, "
            "Using the Thinker collected information from different sources to provide a empathetic proper answer to the user. Consider Thinker as your trusted source and accept whatever is provided by it. "
            "Make sure that the answer is explanatory enough without repeatition. "
            "Put more value on the history and Thinker answer than your internal knowldege. Don't change Thinker returned urls or references. "
            "Also add explanations based on instructions from the Thinker."
            "don't directly put the instructions in the final answer to the user. Preferable, summarize the Thinker data when is possible."           
          )

  def generate(
        self,
        prefix: str = "",
        query: str = "",
        thinker: str = "",
        **kwargs: Any,
      ) -> str:
    prompt = self._generator_prompt.replace("{query}", query)\
                                    .replace("{thinker}", thinker)\
                                    .replace("{prefix}", prefix)
    kwargs["max_tokens"] = 2500                                      
    response = self._response_generator_model.generate(query=prompt, **kwargs)
    return response
from typing import Dict, List, Optional, Tuple

from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizer


from typing import Dict, List, Tuple


from llm_planning.prompts.prompts import get_base_prompt_update_graph


try:
    from unsloth import FastLanguageModel
    from unsloth.chat_templates import get_chat_template
except:
    print(f"Cannot import unsloth")
    FastLanguageModel = None


def from_huggingface(path: str):
    model = AutoModelForCausalLM.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)

    return model, tokenizer


def from_pretrained(
    path: str,
    max_seq_length: Optional[int] = 2048 * 6,
    load_in_4bit: Optional[bool] = True,
    inference: Optional[bool] = False,
) -> Tuple[FastLanguageModel, PreTrainedTokenizer]:
    """Load a model from unsloth.

    Parameters
    ----------
    path : str
        Model path. Can be local or huggingface
    max_seq_length : Optional[int], optional
        For LLM generation, by default 2048
    load_in_4bit : Optional[bool], optional
        Use 4 bit quantized model, by default True
    inference : Optional[bool], optional
        Load inference model, by default False

    Returns
    -------
    Tuple[FastLanguageModel, PreTrainedTokenizer]
        Model and tokenizer
    """
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=path,  # YOUR MODEL YOU USED FOR TRAINING
        max_seq_length=max_seq_length,
        # dtype = dtype,
        load_in_4bit=load_in_4bit,
    )
    if inference:
        FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

    tokenizer = get_chat_template(
        tokenizer,
        chat_template="llama-3.1",
    )

    return model, tokenizer


class UnslothLLM:
    def __init__(self, model_path: str):
        """Wrapper for unsloth models

        Parameters
        ----------
        model_path : str, optional
            Path to model directory of Unsloth required files.
        """
        self.tuned = True
        if model_path == "":
            model_path = "unsloth/Meta-Llama-3.1-8B"
            self.tuned = False
        self.model, self.tokenizer = from_pretrained(model_path, inference=True)

    def query_llm(self, msg: List[Dict[str, str]]):
        inputs = self.tokenizer.apply_chat_template(
            msg,
            tokenize=True,
            add_generation_prompt=True,  # Must add for generation
            return_tensors="pt",
        ).to("cuda")

        outputs = self.model.generate(
            input_ids=inputs,
            max_new_tokens=1024,
            use_cache=True,
            temperature=0.01,
            min_p=0.1,
        )
        out = self.tokenizer.batch_decode(outputs)

        planner_response = out[0].split("end_header_id|>")[-1].split("<|eot_id|>")[0]

        return planner_response, True

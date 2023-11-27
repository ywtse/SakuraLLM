from argparse import ArgumentParser

def parse_args(do_validation:bool=False, add_extra_args_fn:any=None):
    # parse config
    parser = ArgumentParser()
    # server config
    parser.add_argument("--listen", type=str, default="127.0.0.1:5000")
    parser.add_argument("--auth", type=str, help="user:pass, user & pass should not contain ':'")
    parser.add_argument("--no-auth", action="store_true", help="force disable auth")

    # log
    parser.add_argument("-l", "--log", dest="logLevel", choices=[
                        'trace', 'debug', 'info', 'warning', 'error', 'critical'], default="info", help="Set the logging level")

    # model config
    parser.add_argument("--model_name_or_path", type=str,
                        default="SakuraLLM/Sakura-13B-LNovel-v0.8", help="model huggingface id or local path.")
    parser.add_argument("--use_gptq_model", action="store_true", help="whether your model is gptq quantized.")
    parser.add_argument("--model_version", type=str, default="0.8",
                        help="model version written on huggingface readme, now we have ['0.1', '0.4', '0.5', '0.7', '0.8']")
    parser.add_argument("--trust_remote_code", action="store_true", help="whether to trust remote code.")

    parser.add_argument("--llama", action="store_true", help="whether your model is llama family.")

    parser.add_argument("--llama_cpp", action="store_true", help="whether to use llama.cpp.")
    parser.add_argument("--use_gpu", action="store_true", help="whether to use gpu when using llama.cpp.")
    parser.add_argument("--n_gpu_layers", type=int, default=0, help="layers cnt when using gpu in llama.cpp")

    if add_extra_args_fn:
        add_extra_args_fn(parser)

    args = parser.parse_args()

    if do_validation:
        args_validation(args)

    return args


def args_validation(args) -> bool:
    if args.use_gptq_model:
        from auto_gptq import AutoGPTQForCausalLM

    if args.llama_cpp:
        if args.use_gptq_model:
            raise ValueError("You are using both use_gptq_model and llama_cpp flag, which is not supported.")
        from llama_cpp import Llama

    if args.llama:
        from transformers import LlamaForCausalLM, LlamaTokenizer

    if args.trust_remote_code is False and args.model_version in "0.5 0.7 0.8":
        raise ValueError("If you use model version 0.5, 0.7 or 0.8, please add flag --trust_remote_code.")

    return True
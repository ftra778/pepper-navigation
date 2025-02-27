# #!/bin/bash

# CHECKPOINT_DIR=~/.llama/checkpoints/Meta-Llama3.2-3B
# PYTHONPATH=$(git rev-parse --show-toplevel) torchrun llama_models/scripts/example_chat_completion.py $CHECKPOINT_DIR
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# top-level folder for each specific model found within the models/ directory at
# the top-level of this source tree.

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed in accordance with the terms of the Llama 3 Community License Agreement.

from typing import Optional
import os

import fire

from llama_models.llama3.api.datatypes import RawMessage, StopReason

from llama_models.llama3.reference_impl.generation import Llama

os.environ['RANK'] = '0'

def run_main(
    # ckpt_dir = f"{os.path.expanduser("~")}/.llama/checkpoints/Meta-Llama3.2-3B",
    ckpt_dir = os.path.expanduser("~") + "/.llama/checkpoints/Llama3.2-3B",
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
    model_parallel_size: Optional[int] = None,
):
    """
    Examples to run with the models finetuned for chat. Prompts correspond of chat
    turns between the user and assistant with the final one always being the user.

    An optional system prompt at the beginning to control how the model should respond
    is also supported.

    `max_gen_len` is optional because finetuned models are able to stop generations naturally.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
        model_parallel_size=model_parallel_size,
    )
    
    while True:
        prompt = [RawMessage(role="user", content=input(">>"))]
                # RawMessage(role="system", content="You are a robot whose name is Pepper. You are a guide robot for The University of Auckland's CARES lab"),
                
        result = generator.chat_completion(
            prompt,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        print(result.generation.content)

    # # for msg in dialog:
    # # print(f"{prompt.role.capitalize()}: {prompt.content}\n")

    #     out_message = result.generation
    #     print(out_message)
        # print(f"{prompt.role.capitalize()}: {prompt.content}\n")

        # out_message = result.generation
        # print(f"> {out_message.role.capitalize()}: {out_message.content}")
        # print("\n==================================\n")
    # print(out_message)
    # print(f"> {out_message.role.capitalize()}: {out_message.content}")
    # print("\n==================================\n")

#     dialogs = [
#         [RawMessage(role="user", content="what is the recipe of mayonnaise?")],
#         [
#             RawMessage(
#                 role="user",
#                 content="I am going to Paris, what should I see?",
#             ),
#             RawMessage(
#                 role="assistant",
#                 content="""\
# Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:

# 1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.
# 2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.
# 3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.

# These are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.""",
#                 stop_reason=StopReason.end_of_turn,
#             ),
#             RawMessage(role="user", content="What is so great about #1?"),
#         ],
#         [
#             RawMessage(role="system", content="Always answer with Haiku"),
#             RawMessage(role="user", content="I am going to Paris, what should I see?"),
#         ],
#         [
#             RawMessage(role="system", content="Always answer with emojis"),
#             RawMessage(role="user", content="How to go from Beijing to NY?"),
#         ],
#     ]
#     for dialog in dialogs:
#         result = generator.chat_completion(
#             dialog,
#             max_gen_len=max_gen_len,
#             temperature=temperature,
#             top_p=top_p,
#         )

#         for msg in dialog:
#             print(f"{msg.role.capitalize()}: {msg.content}\n")

#         out_message = result.generation
#         print(f"> {out_message.role.capitalize()}: {out_message.content}")
#         print("\n==================================\n")



def main():
    fire.Fire(run_main)


if __name__ == "__main__":
    main()

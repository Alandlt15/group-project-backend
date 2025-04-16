import sys
import openai
import json
import pathlib
import loguru
from constant.chromosome import Chromosome
from iterative_prompt_optimization import IterativePromptOptimizer
from intention.base_intention import Intention
from harness.base_harness import Harness
from harness.custom_harness import TestHarness
from intention.custom_intention import TestIntention

logger = loguru.logger
logger.add(sys.stdout, level="INFO") 

# Load config file from root path
config_file_path = pathlib.Path("./config.json")
# Read config file
config = json.load(open(config_file_path))

# Initialize OpenAI API key
openai.api_key = config["openai_key"]

# Define constants for optimization process
max_iteration = 2
max_crossover = 0.1
max_mutation = 0.5
max_population = 10


def inject(intention: Intention, application_harness: Harness) -> Chromosome:
    # Create and run an IterativePromptOptimizer instance to optimize prompts
    iterative_prompt_optimizer = IterativePromptOptimizer(
        intention,
        application_harness,
        max_iteration,
        max_crossover,
        max_mutation,
        max_population,
    )
    iterative_prompt_optimizer.optimize()
    return iterative_prompt_optimizer.best_chromosome


def main():
    # Initialize prompt injection intention and harness
    content_manipulation = TestIntention()
    application_harness = TestHarness()

    # Begin the prompt injection process
    chromosome = inject(content_manipulation, application_harness)

    logger.info("Finish injection")
    if chromosome is None:
        logger.error("Failed to inject prompt, please check the log for more details")

    # Log the results of the injection
    if chromosome.is_successful:
        logger.info(
            f"Success! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    else:
        logger.info(
            f"Failed! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    logger.info(f"Fitness Score: {chromosome.fitness_score}")
    logger.info(f"Response: {chromosome.llm_response}")


if __name__ == "__main__":
    main()


# # Load config file from root path
# config_file_path = pathlib.Path("./config.json")
# # Read config file
# config = json.load(open(config_file_path))

# # Initialize OpenAI API key
# openai.api_key = config["openai_key"]

# # Optimization parameters
# max_iteration = 50
# max_crossover = 0.1
# max_mutation = 0.5
# max_population = 10

# def load_class_from_file(filepath):
#     """
#     Dynamically load a class from a given file path.
#     Returns an instance of the first class found in the file.
#     """
#     spec = importlib.util.spec_from_file_location("custom_module", filepath)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)

#     for attr_name in dir(module):
#         attr = getattr(module, attr_name)
#         if isinstance(attr, type):
#             return attr()
#     raise Exception(f"No class found in file: {filepath}")

# def inject(intention, harness) -> Chromosome:
#     optimizer = IterativePromptOptimizer(
#         intention,
#         harness,
#         max_iteration,
#         max_crossover,
#         max_mutation,
#         max_population
#     )
#     optimizer.optimize()
#     return optimizer.best_chromosome

# def main():
#     print("here")
#     if len(sys.argv) != 3:
#         print("Usage: python custom_main.py <harness_path> <intention_path>")
#         sys.exit(1)

#     harness_path = sys.argv[1]
#     intention_path = sys.argv[2]
#     print(intention_path)
#     print(harness_path)

#     # Load classes
#     harness = load_class_from_file(harness_path)
#     intention = load_class_from_file(intention_path)

#     print(f"harness code: {harness}")
#     print(f"intention code: {intention}")

#     # Run optimization
#     best = inject(intention, harness)

#     # Output results
#     print("Injection Complete")
#     print("Injected Prompt:", best.framework, best.separator, best.disruptor)
#     print("Fitness Score:", best.fitness_score)
#     print("LLM Response:", best.llm_response)

# if __name__ == "__main__":
#     main()

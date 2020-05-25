from runtime_syspath import print_syspath

# What is this expected to show?
print_syspath(sort=False)
#    vvv - Don't ever do that... stay tuned.
from src.run_the_project_main import main_reusable_func

if __name__ == "__main__":
    print(main_reusable_func())

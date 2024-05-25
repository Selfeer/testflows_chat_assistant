question_and_answer = [
    (
        "What is the TestFlows?",
        """TestFlows is an open-source software testing framework that supports various types of testing such as functional, integration, acceptance, and unit testing. It allows test authors to explicitly define test flows using Python code, leveraging an "everything is a test" approach to provide flexibility in writing and executing tests. It is suitable for both small and large QA groups, featuring integration with tools like ClickHouse and Grafana for analytics, and supports self-documenting tests using behavior-driven step keywords.

```python
# Example of a simple test using TestFlows
from testflows.core import Test, Given, When, Then

with Test("Example Test"):
    with Given("I have a function to test"):
        def add(a, b):
            return a + b

    with When("I add 2 and 3"):
        result = add(2, 3)

    with Then("the result should be 5"):
        assert result == 5, "Expected result to be 5"
""",
    ),
    (
        "How do I run the TestFlows tests in parallel?",
        """To run TestFlows tests in parallel, you need to set the `parallel=True` flag during the test definition or use the `[PARALLEL]` flag. Additionally, you can specify an executor using the `executor` parameter to control the parallel execution. If no executor is specified, a default executor appropriate for the test type is created automatically.

Here is an example of how you might define and run parallel tests:

```python
from testflows.core import TestModule, TestScenario, parallel

@TestModule
@parallel
def my_parallel_tests_module(self):
    with Scenario("Test 1", parallel=True):
        # Test logic here

    with Scenario("Test 2", parallel=True):
        # Test logic here

if __name__ == "__main__":
    my_parallel_tests_module()
```

This example sets the whole module to run tests in parallel and each scenario within the module also explicitly marked to run in parallel.""",
    ),
]

# Brief Folder information
This folder contains the project tests using pytest.

# How to run
from the root directory run:
```
$ make run_tests
```

See the make file for the full command

# Conventions
## Tests file
Must be placed inside `tests\tests\`. This prevents mixing up with the tests config files and reports in `tests\`.

## Test functions docstring
The docstring for the test functions follows the convention:
```
GIVEN: {Test initial conditions}
WHEN: {What needs to be tested}
THEN: {The expected response}
{Additional information}
```

See the test files for examples.

## Coverage reports
- coverage report files/folder must end with "_coverage_report".
 For example, an HTML report should be named "html_coverage_report".


# Useful links
- [Overall testing with pytest](https://www.youtube.com/watch?v=OcD52lXq0e8)
- [Unit vs Functional tests](https://stackoverflow.com/a/2741845/14593213)
- [Pytest and coverage report](https://pytest-cov.readthedocs.io/en/latest/reporting.html)
- [Coverage config file](https://coverage.readthedocs.io/en/latest/config.html#)
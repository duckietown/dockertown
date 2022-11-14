import dockertown.utils


def test_project_root():
    assert (dockertown.utils.PROJECT_ROOT / "setup.py").exists()


def test_environment_variables_propagation(monkeypatch):
    monkeypatch.setenv("SOME_VARIABLE", "dododada")

    stdout = dockertown.utils.run(
        ["bash", "-c", "echo $SOME_VARIABLE && echo $OTHER_VARIABLE"],
        capture_stdout=True,
        env={"OTHER_VARIABLE": "dudu"},
    )
    assert stdout == "dododada\ndudu"

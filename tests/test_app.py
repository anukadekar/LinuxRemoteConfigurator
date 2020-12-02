from context import linux_remote_configurator


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    linux_remote_configurator.LinuxRemoteConfigurator.run()
    captured = capsys.readouterr()

    assert "Hello, World!!" in captured.out

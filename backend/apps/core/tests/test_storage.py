from django.core.management import call_command


def test_ensure_buckets_skips_without_s3(settings, capsys):
    settings.USE_S3 = False
    call_command("ensure_buckets")
    assert "local disk" in capsys.readouterr().out

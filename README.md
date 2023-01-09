> https://sosheskaz.github.io/tutorial/2016/09/26/Avahi-HTTP-Service.html

`/etc/avahi/services/loadreporter.service`に、以下を書きこむ。

```xml
<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h LoadReporter</name>
  <service>
    <type>_loadreporter._tcp</type>
    <port>8086</port>
  </service>
</service-group>
```

そして、各マシン上で、最低限の稼働状況を知らせるFastAPIを準備する。(LoadReporter)

LoadMetersサーバは、LoadReporterにときどき問いあわせて、その情報を一括してSvelteに流す。

AVAHIのサービスをPythonでリストすることはできるか? zeroconfでできる。

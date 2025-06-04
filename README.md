# tdengineDemo

Use Case: Simulated real-time temperature, humidity, and vibration data from a factory machine sensor.

5. Connect TDengine to Grafana
   • Launch Grafana (self-hosted or Grafana Cloud).
   • Install the TDengine datasource plugin.
   • Connect it using your TDengine Cloud credentials.
   • Create a dashboard with:
   • Time series panels for temperature, humidity, vibration.

export TDENGINE_CLOUD_URL="https://yourcluster.tdengine.cloud"
export TDENGINE_CLOUD_TOKEN="your-auth-token-from-cloud-console"
https://cloud.tdengine.com/explorer

/opt/homebrew/opt/grafana/bin/grafana-server \
 --config=/opt/homebrew/etc/grafana/grafana.ini \
 --homepath=/opt/homebrew/share/grafana \
 --packaging=brew

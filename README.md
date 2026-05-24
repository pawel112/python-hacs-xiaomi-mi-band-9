# Xiaomi Mi Band 9 — Home Assistant Integration

Integracja grupuje encje z aplikacji **Notify for Mi Band** pod jednym urządzeniem "Xiaomi Mi Band 9" w Home Assistant.

## Wymagania

- Home Assistant 2023.1+
- Aplikacja [Notify for Mi Band](https://play.google.com/store/apps/details?id=com.mc.miband1) na telefonie z włączoną integracją HA

## Instalacja przez HACS

1. Otwórz HACS → **Integracje** → trzy kropki ⋮ → **Repozytoria niestandardowe**
2. Wklej URL tego repozytorium, kategoria: **Integration**
3. Kliknij **Dodaj** → znajdź "Xiaomi Mi Band 9" → **Pobierz**
4. Uruchom ponownie Home Assistant
5. Przejdź do **Ustawienia → Urządzenia i usługi → Dodaj integrację** → wyszukaj "Xiaomi Mi Band 9"

## Instalacja ręczna

Skopiuj folder `custom_components/xiaomi_mi_band_9/` do folderu `config/custom_components/` w Home Assistant i uruchom ponownie.

## Encje

| Encja | Typ | Opis |
|-------|-----|------|
| `sensor.bateria` | sensor | Poziom naładowania baterii (%) |
| `sensor.kroki` | sensor | Liczba kroków |
| `sensor.tetno` | sensor | Tętno (bpm) |
| `sensor.sen` | sensor | Czas snu (min) |
| `sensor.spo2` | sensor | Saturacja krwi (%) |
| `sensor.stres` | sensor | Poziom stresu |
| `sensor.aktywnosc` | sensor | Wynik aktywności |
| `sensor.ostatnie_polaczenie` | sensor | Znacznik czasu ostatniego połączenia |
| `sensor.ostatnie_rozlaczenie` | sensor | Znacznik czasu ostatniego rozłączenia |
| `binary_sensor.polaczony` | binary_sensor | Czy opaska jest połączona |

## Encje źródłowe (Notify for Mi Band)

Integracja odczytuje następujące encje:

| Encja źródłowa | Dane |
|----------------|------|
| `sensor.miband_battery` | Bateria |
| `sensor.miband_steps` | Kroki |
| `sensor.miband_heartrate` | Tętno |
| `sensor.miband_sleep` | Sen |
| `sensor.miband_spo2` | SpO2 |
| `sensor.miband_stress` | Stres |
| `sensor.miband_as` | Aktywność |
| `sensor.miband_trigger_6` | Timestamp połączenia |
| `sensor.miband_trigger_7` | Timestamp rozłączenia |

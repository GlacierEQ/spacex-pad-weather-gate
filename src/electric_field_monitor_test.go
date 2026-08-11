package weather

import (
	"math"
	"testing"
)

func TestMonitorRejectsInvalidThresholdAndReadings(t *testing.T) {
	if _, err := NewElectricFieldMonitor(0); err == nil {
		t.Fatal("zero threshold must fail")
	}
	monitor, err := NewElectricFieldMonitor(1.5)
	if err != nil {
		t.Fatalf("unexpected monitor error: %v", err)
	}
	if err := monitor.UpdateSensor("", "fixture", 0.2); err == nil {
		t.Fatal("empty sensor id must fail")
	}
	if err := monitor.UpdateSensor("sensor-a", "fixture", math.NaN()); err == nil {
		t.Fatal("NaN field reading must fail")
	}
}

func TestMonitorUsesMaximumAbsoluteSyntheticReading(t *testing.T) {
	monitor, err := NewElectricFieldMonitor(1.5)
	if err != nil {
		t.Fatalf("unexpected monitor error: %v", err)
	}
	if err := monitor.UpdateSensor("a", "west", -0.8); err != nil {
		t.Fatal(err)
	}
	if err := monitor.UpdateSensor("b", "east", 1.6); err != nil {
		t.Fatal(err)
	}
	if got := monitor.MaxElectricField(); got != 1.6 {
		t.Fatalf("unexpected max field: %v", got)
	}
	if !monitor.IsThresholdExceeded() {
		t.Fatal("threshold should be exceeded")
	}
}

func TestIllustrativeConstraintEvaluation(t *testing.T) {
	goState := EnvironmentalState{
		SurfaceWindKts:    10,
		UpperWindKts:      30,
		ElectricFieldKVm:  0.2,
		NearbyStrikeCount: 0,
		CloudCeilingFt:    5000,
		TemperatureF:      70,
		Precipitation:     false,
	}
	ok, violations, err := EvaluateConstraints(goState)
	if err != nil || !ok || len(violations) != 0 {
		t.Fatalf("expected local pass: ok=%v violations=%v err=%v", ok, violations, err)
	}

	blocked := goState
	blocked.ElectricFieldKVm = -2.0
	blocked.NearbyStrikeCount = 1
	ok, violations, err = EvaluateConstraints(blocked)
	if err != nil || ok {
		t.Fatalf("expected local block: ok=%v violations=%v err=%v", ok, violations, err)
	}
	if len(violations) != 2 || violations[0] != "electric_field" || violations[1] != "nearby_strike" {
		t.Fatalf("unexpected violations: %v", violations)
	}
}

func TestConstraintStateRejectsMalformedValues(t *testing.T) {
	_, _, err := EvaluateConstraints(EnvironmentalState{SurfaceWindKts: math.Inf(1)})
	if err == nil {
		t.Fatal("infinite state value must fail")
	}
	_, _, err = EvaluateConstraints(EnvironmentalState{NearbyStrikeCount: -1})
	if err == nil {
		t.Fatal("negative strike count must fail")
	}
}

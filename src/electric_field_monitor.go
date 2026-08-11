// Package weather implements repository-local environmental constraint helpers.
// It does not implement SpaceX Launch Commit Criteria, range-safety rules, or
// real pad-sensor acquisition.
package weather

import (
	"errors"
	"math"
	"sync"
	"time"
)

const EvidenceState = "LOCAL_ENVIRONMENTAL_RULE_GATE_NOT_LAUNCH_SAFETY_AUTHORITY"

// FieldReading is one caller-supplied synthetic electric-field observation.
type FieldReading struct {
	SensorID     string
	LocationName string
	FieldKVPerM  float64
	Timestamp    time.Time
}

// EnvironmentalState is a caller-supplied synthetic state for illustrative
// rule evaluation. Its thresholds are portfolio fixtures, not official limits.
type EnvironmentalState struct {
	SurfaceWindKts    float64
	UpperWindKts      float64
	ElectricFieldKVm  float64
	NearbyStrikeCount int
	CloudCeilingFt    float64
	TemperatureF      float64
	Precipitation     bool
}

// ElectricFieldMonitor aggregates in-memory caller-supplied readings.
type ElectricFieldMonitor struct {
	mu          sync.RWMutex
	sensors     map[string]FieldReading
	thresholdKV float64
}

func finite(value float64) bool {
	return !math.IsNaN(value) && !math.IsInf(value, 0)
}

// NewElectricFieldMonitor creates a local threshold monitor.
func NewElectricFieldMonitor(thresholdKV float64) (*ElectricFieldMonitor, error) {
	if !finite(thresholdKV) || thresholdKV <= 0 {
		return nil, errors.New("threshold must be finite and positive")
	}
	return &ElectricFieldMonitor{
		sensors:     make(map[string]FieldReading),
		thresholdKV: thresholdKV,
	}, nil
}

// UpdateSensor stores a synthetic reading. It performs no external polling.
func (m *ElectricFieldMonitor) UpdateSensor(id string, location string, fieldKV float64) error {
	if id == "" {
		return errors.New("sensor id required")
	}
	if !finite(fieldKV) {
		return errors.New("field value must be finite")
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	m.sensors[id] = FieldReading{
		SensorID:     id,
		LocationName: location,
		FieldKVPerM:  fieldKV,
		Timestamp:    time.Now(),
	}
	return nil
}

// MaxElectricField returns the maximum absolute value among stored readings.
func (m *ElectricFieldMonitor) MaxElectricField() float64 {
	m.mu.RLock()
	defer m.mu.RUnlock()
	maxField := 0.0
	for _, sensor := range m.sensors {
		if magnitude := math.Abs(sensor.FieldKVPerM); magnitude > maxField {
			maxField = magnitude
		}
	}
	return maxField
}

// IsThresholdExceeded compares local in-memory readings to the configured
// illustrative threshold.
func (m *ElectricFieldMonitor) IsThresholdExceeded() bool {
	return m.MaxElectricField() >= m.thresholdKV
}

func validateState(state EnvironmentalState) error {
	values := []float64{
		state.SurfaceWindKts,
		state.UpperWindKts,
		state.ElectricFieldKVm,
		state.CloudCeilingFt,
		state.TemperatureF,
	}
	for _, value := range values {
		if !finite(value) {
			return errors.New("environmental values must be finite")
		}
	}
	if state.SurfaceWindKts < 0 || state.UpperWindKts < 0 || state.CloudCeilingFt < 0 {
		return errors.New("wind and ceiling values must be non-negative")
	}
	if state.NearbyStrikeCount < 0 {
		return errors.New("strike count must be non-negative")
	}
	return nil
}

// EvaluateConstraints applies illustrative local fixture thresholds.
func EvaluateConstraints(state EnvironmentalState) (bool, []string, error) {
	if err := validateState(state); err != nil {
		return false, nil, err
	}
	violations := make([]string, 0)
	if state.SurfaceWindKts > 30.0 {
		violations = append(violations, "surface_wind")
	}
	if state.UpperWindKts > 140.0 {
		violations = append(violations, "upper_wind")
	}
	if math.Abs(state.ElectricFieldKVm) >= 1.5 {
		violations = append(violations, "electric_field")
	}
	if state.NearbyStrikeCount > 0 {
		violations = append(violations, "nearby_strike")
	}
	if state.TemperatureF < 40.0 {
		violations = append(violations, "temperature")
	}
	if state.Precipitation {
		violations = append(violations, "precipitation")
	}
	return len(violations) == 0, violations, nil
}

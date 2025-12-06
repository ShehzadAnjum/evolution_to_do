#!/bin/bash
# scripts/check-feature-necessity.sh
# Interactive checklist before starting new feature

echo "🎯 Feature Necessity Test"
echo ""
echo "Feature Name: "
read FEATURE_NAME
echo ""

echo "Answer YES/NO for each question:"
echo ""

echo "1. Phase Alignment: Is this in current phase spec?"
read -p "   Answer: " Q1
echo ""

echo "2. Dependency Met: Do I have all prerequisites?"
read -p "   Answer: " Q2
echo ""

echo "3. Value Now: Does this deliver value with current functionality?"
read -p "   Answer: " Q3
echo ""

echo "4. Spec Defined: Is this specified in specs/ folder?"
read -p "   Answer: " Q4
echo ""

# Check if all YES
if [[ "$Q1" =~ ^[Yy]$ ]] && [[ "$Q2" =~ ^[Yy]$ ]] && [[ "$Q3" =~ ^[Yy]$ ]] && [[ "$Q4" =~ ^[Yy]$ ]]; then
    echo "✅ PROCEED: All checks passed"
    echo "Feature '$FEATURE_NAME' is necessary and ready to implement"
    exit 0
else
    echo "❌ DEFER: One or more checks failed"
    echo "Feature '$FEATURE_NAME' should be deferred"
    echo ""
    echo "Recommended action:"
    if [[ ! "$Q1" =~ ^[Yy]$ ]]; then
        echo "  - Wait until correct phase"
    fi
    if [[ ! "$Q2" =~ ^[Yy]$ ]]; then
        echo "  - Implement missing dependencies first"
    fi
    if [[ ! "$Q3" =~ ^[Yy]$ ]]; then
        echo "  - Wait until prerequisite features exist"
    fi
    if [[ ! "$Q4" =~ ^[Yy]$ ]]; then
        echo "  - Write specification first"
    fi
    exit 1
fi


#!/bin/bash

# ADR Management Script
# Usage: ./create-adr.sh "Your ADR Title" "Author Name"

set -e

# Configuration
ADR_DIR="docs/adrs"
ADR_TEMPLATE="# {number}. {title}

Date: {date}

Author: {author}

## Status

Proposed

## Context

<!-- Describe the context and problem statement -->

## Decision

<!-- Describe the architectural decision -->

## Consequences

<!-- Describe the resulting context and consequences -->
"

# Function to display usage
usage() {
    echo "Usage: $0 \"ADR Title\" \"Author Name\""
    echo "Example: $0 \"Use PostgreSQL for data persistence\" \"John Doe\""
    exit 1
}

# Function to convert title to lowercase hyphen-separated format
format_title() {
    local title="$1"
    echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g'
}

# Function to get the next ADR number
get_next_adr_number() {
    if [ ! -d "$ADR_DIR" ]; then
        echo 1
        return
    fi
    
    # Find all ADR files and extract numbers
    local max_num=0
    
    # Check if any .md files exist first
    if ls "$ADR_DIR"/*.md >/dev/null 2>&1; then
        for file in "$ADR_DIR"/*.md; do
            if [ -f "$file" ]; then
                # Extract number from filename (assuming format: NNNN-title.md)
                local num=$(basename "$file" .md | grep -o '^[0-9]*' | sed 's/^0*//')
                if [ -n "$num" ] && [ "$num" -gt "$max_num" ]; then
                    max_num=$num
                fi
            fi
        done
    fi
    
    echo $((max_num + 1))
}

# Function to pad number with zeros
pad_number() {
    printf "%04d" "$1"
}

# Check arguments
if [ $# -ne 2 ]; then
    echo "Error: Both title and author name are required."
    usage
fi

TITLE="$1"
AUTHOR="$2"

# Validate inputs
if [ -z "$TITLE" ]; then
    echo "Error: Title cannot be empty."
    usage
fi

if [ -z "$AUTHOR" ]; then
    echo "Error: Author name cannot be empty."
    usage
fi

# Get current date
CURRENT_DATE=$(date +"%Y-%m-%d")

# Create ADR directory if it doesn't exist
mkdir -p "$ADR_DIR"

# Get next ADR number and format it
ADR_NUMBER=$(get_next_adr_number)
PADDED_NUMBER=$(pad_number "$ADR_NUMBER")

# Format title for filename
FORMATTED_TITLE=$(format_title "$TITLE")

# Create filename
FILENAME="${PADDED_NUMBER}-${FORMATTED_TITLE}.md"
FILEPATH="${ADR_DIR}/${FILENAME}"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo "Error: ADR file already exists: $FILEPATH"
    exit 1
fi

# Create ADR content from template
ADR_CONTENT=$(echo "$ADR_TEMPLATE" | sed "s/{number}/$ADR_NUMBER/g" | sed "s/{title}/$TITLE/g" | sed "s/{date}/$CURRENT_DATE/g" | sed "s/{author}/$AUTHOR/g")

# Write ADR file
echo "$ADR_CONTENT" > "$FILEPATH"

# Success message
echo "ADR created successfully!"
echo "File: $FILEPATH"
echo "Number: $ADR_NUMBER"
echo "Title: $TITLE"
echo "Author: $AUTHOR"
echo "Date: $CURRENT_DATE"

# Optional: Open the file in default editor if EDITOR is set
if [ -n "$EDITOR" ]; then
    read -p "Open the ADR in your editor? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $EDITOR "$FILEPATH"
    fi
fi
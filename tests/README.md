# Tests Directory

This directory contains all test files for the TCG Nerd Bot project.

## Test Categories

### Core Functionality Tests
- `test_integration.py` - Integration tests for main features
- `test_quick.py` - Quick functionality validation
- `simple_test.py` - Basic functionality tests

### Commander Game Tests
- `test_setcommander_no_id.py` - Commander setting without game ID
- `test_commander_colors.py` - Commander color identification
- `test_reaction_placement.py` - Placement reaction handling
- `test_selection.py` - Selection mechanism tests

### EDHREC API Tests
- `test_edhrec.py` - Basic EDHREC API tests
- `test_edhrec_comprehensive.py` - Comprehensive EDHREC testing
- `test_edhrec_quick.py` - Quick EDHREC API validation
- `test_edhrec_simple.py` - Simple EDHREC functionality
- `test_improved_edhrec.py` - Tests for improved EDHREC implementation
- `test_tags_extraction.py` - EDHREC Tags extraction tests
- `test_normalization.py` - Archetype normalization tests

### Archetype System Tests
- `test_archetype_system.py` - Complete archetype system tests
- `test_archetype_reactions.py` - Archetype reaction handling tests
- `test_archetype_emojis.py` - Emoji mapping functionality
- `test_archetype_integration.py` - Archetype integration tests

### UI/UX Tests  
- `test_help_command.py` - Help command functionality
- `test_help_embed.py` - Help embed generation
- `test_help_pagination.py` - Paginated help system
- `test_enhanced_commands.py` - Enhanced command features
- `test_emojis.py` - Emoji functionality tests

### Analytics & Achievements Tests
- `test_analytics_achievements.py` - Analytics and achievement system tests

### Collection Management Tests
- `test_compareall.py` - Collection comparison tests

## Running Tests

To run individual tests:
```bash
python test_filename.py
```

To run all tests in a category, navigate to the tests directory and run the relevant test files.

## Test Guidelines

- Tests should be self-contained and not depend on external state
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Mock external API calls when possible for faster testing

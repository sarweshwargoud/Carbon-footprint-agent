# Requirements Document

## Introduction

The Carbon Footprint Reduction Agent is a web-based sustainability application that empowers users to understand and reduce their environmental impact. The system collects user consumption data across five key categories (electricity, transport, food, waste, and water), calculates monthly and yearly CO2 emissions using scientifically-backed emission factors, identifies the highest emission source, and provides AI-driven personalized advice with actionable steps for carbon reduction. The application features an interactive Streamlit interface with real-time visualizations, sustainability status assessment, and report export capabilities.

## Glossary

- **System**: The Carbon Footprint Reduction Agent application
- **Calculator_Module**: The component responsible for CO2 emission calculations
- **Agent_Module**: The component responsible for generating AI-driven advice and recommendations
- **RAG_Engine**: The Retrieval-Augmented Generation engine using keyword-based search on local knowledge base
- **UI_Component**: The Streamlit-based user interface
- **Emission_Factor**: A coefficient representing kg CO2 emitted per unit of consumption
- **Breakdown**: A dictionary containing CO2 emissions for each category and totals
- **Highest_Source**: The consumption category contributing the largest percentage of total emissions
- **Knowledge_Base**: Collection of text files containing sustainability tips and emission data
- **User_Report**: JSON-formatted export containing emission calculations and analysis

## Requirements

### Requirement 1: Emission Calculation

**User Story:** As a user, I want to calculate my carbon footprint based on monthly consumption data, so that I can understand my environmental impact.

#### Acceptance Criteria

1. WHEN a user provides electricity consumption in kWh, THE Calculator_Module SHALL calculate CO2 emissions using the emission factor of 0.82 kg CO2 per kWh
2. WHEN a user provides transport data (petrol, diesel, bus, train, flight), THE Calculator_Module SHALL calculate total transport CO2 emissions by summing individual contributions
3. WHEN a user provides diet type (vegetarian or non-vegetarian) and number of days, THE Calculator_Module SHALL calculate food-related CO2 emissions
4. WHEN a user provides waste data (plastic and e-waste in kg), THE Calculator_Module SHALL calculate waste-related CO2 emissions
5. WHEN a user provides water consumption in cubic meters, THE Calculator_Module SHALL calculate water-related CO2 emissions
6. WHEN all consumption data is provided, THE Calculator_Module SHALL calculate monthly total CO2 emissions by summing all categories
7. WHEN monthly total is calculated, THE Calculator_Module SHALL calculate yearly projection by multiplying monthly total by 12
8. WHEN calculations are complete, THE Calculator_Module SHALL return breakdown with rounded values to 2 decimal places

### Requirement 2: Emission Analysis

**User Story:** As a user, I want to see which category contributes most to my carbon footprint, so that I can prioritize reduction efforts.

#### Acceptance Criteria

1. WHEN monthly emissions are calculated, THE Calculator_Module SHALL compute percentage contribution for each category
2. WHEN percentages are computed, THE Calculator_Module SHALL identify the category with the highest percentage as the highest emission source
3. WHEN monthly total is zero, THE Calculator_Module SHALL set all percentages to zero
4. WHEN percentages are calculated, THE Calculator_Module SHALL round each percentage to 2 decimal places

### Requirement 3: AI-Driven Advice Generation

**User Story:** As a user, I want to receive personalized sustainability advice based on my highest emission source, so that I can take targeted action to reduce my footprint.

#### Acceptance Criteria

1. WHEN the highest emission source is identified, THE Agent_Module SHALL map the source to relevant search keywords
2. WHEN search keywords are determined, THE Agent_Module SHALL retrieve relevant tips from the Knowledge_Base using keyword matching
3. WHEN tips are retrieved, THE Agent_Module SHALL select up to 5 random tips to provide dynamic recommendations
4. WHEN no tips are found, THE Agent_Module SHALL provide a default recommendation for conducting an energy audit
5. WHEN tips are formatted, THE Agent_Module SHALL include the highest source name and its percentage contribution
6. IF the Knowledge_Base directory does not exist, THEN THE Agent_Module SHALL return an error message indicating the knowledge base is not found

### Requirement 4: Decision Explanation

**User Story:** As a user, I want to understand why the AI selected a particular category as my main problem, so that I can trust the system's recommendations.

#### Acceptance Criteria

1. WHEN the highest emission source is identified, THE Agent_Module SHALL generate an explanation including the CO2 amount and percentage
2. WHEN generating explanation, THE Agent_Module SHALL list all five categories being compared
3. WHEN explanation is complete, THE Agent_Module SHALL clearly state that the highest percentage determines priority

### Requirement 5: Actionable Steps Generation

**User Story:** As a user, I want to receive specific, time-bound action steps, so that I can implement changes immediately and plan long-term improvements.

#### Acceptance Criteria

1. WHEN the highest emission source is identified, THE Agent_Module SHALL generate three types of actions: immediate, weekly, and long-term
2. WHEN generating actions for electricity, THE Agent_Module SHALL recommend unplugging devices, LED replacement, and solar investment
3. WHEN generating actions for transport, THE Agent_Module SHALL recommend tire pressure checks, carpooling, and EV adoption
4. WHEN generating actions for food, THE Agent_Module SHALL recommend meat-free meals, local sourcing, and plant-based diet
5. WHEN generating actions for waste, THE Agent_Module SHALL recommend waste segregation, reusable items, and composting
6. WHEN generating actions for water, THE Agent_Module SHALL recommend tap discipline, leak fixing, and rainwater harvesting

### Requirement 6: Data Visualization

**User Story:** As a user, I want to see visual representations of my emissions breakdown, so that I can quickly understand my consumption patterns.

#### Acceptance Criteria

1. WHEN emission calculations are complete, THE UI_Component SHALL display monthly total, yearly projection, and top contributor as metrics
2. WHEN displaying metrics, THE UI_Component SHALL show the top contributor with an inverse delta indicator
3. WHEN breakdown data is available, THE UI_Component SHALL render a bar chart showing emissions for all five categories
4. WHEN rendering the bar chart, THE UI_Component SHALL use category names as labels and emission values in kg CO2

### Requirement 7: User Input Collection

**User Story:** As a user, I want to input my monthly consumption data through an intuitive interface, so that I can easily calculate my carbon footprint.

#### Acceptance Criteria

1. WHEN the application loads, THE UI_Component SHALL display input fields for electricity (kWh), water (m³), petrol (L), diesel (L), diet type, plastic waste (kg), and e-waste (kg)
2. WHEN the application loads, THE UI_Component SHALL provide an expandable section for public transport inputs (bus km, train km, flight km)
3. WHEN a user hovers over input fields, THE UI_Component SHALL apply visual feedback with transform and shadow effects
4. WHEN a user clicks the calculate button, THE UI_Component SHALL display a loading spinner with the message "Analyzing your lifestyle..."
5. WHEN input fields are displayed, THE UI_Component SHALL set default values (electricity: 300 kWh, water: 10 m³, petrol: 40 L, plastic: 5 kg)

### Requirement 8: Sustainability Status Assessment

**User Story:** As a user, I want to see my overall sustainability status, so that I can understand how my footprint compares to benchmarks.

#### Acceptance Criteria

1. WHEN yearly total is less than 2000 kg CO2, THE UI_Component SHALL display a success message indicating "Eco-Warrior" status
2. WHEN yearly total is between 2000 and 4000 kg CO2, THE UI_Component SHALL display a warning message indicating "Average" status
3. WHEN yearly total is greater than 4000 kg CO2, THE UI_Component SHALL display an error message indicating "High Impact" status
4. WHEN sustainability status is displayed, THE UI_Component SHALL calculate and show potential savings from 30% reduction in the highest source

### Requirement 9: Report Export

**User Story:** As a user, I want to export my carbon footprint report, so that I can track my progress over time or share results.

#### Acceptance Criteria

1. WHEN a user clicks "Save to System", THE UI_Component SHALL create a JSON report containing breakdown, percentages, highest source, and timestamp
2. WHEN saving to system, THE UI_Component SHALL create the outputs/user_reports directory if it does not exist
3. WHEN saving to system, THE UI_Component SHALL generate a filename with format "report_YYYYMMDD_HHMMSS.json"
4. WHEN a user clicks "Download JSON", THE UI_Component SHALL provide a downloadable JSON file with the same report structure
5. WHEN download is initiated, THE UI_Component SHALL use filename format "carbon_report_YYYYMMDD.json"
6. IF saving to system fails, THEN THE UI_Component SHALL display an error message with the exception details

### Requirement 10: Knowledge Base Retrieval

**User Story:** As a developer, I want the system to retrieve sustainability tips from local text files, so that the application can provide advice without requiring external APIs or heavy ML dependencies.

#### Acceptance Criteria

1. WHEN retrieving tips, THE Agent_Module SHALL search all .txt files in the rag_docs directory
2. WHEN searching files, THE Agent_Module SHALL perform case-insensitive keyword matching
3. WHEN a line matches any keyword, THE Agent_Module SHALL add the line to results if it is not empty and not a duplicate
4. WHEN reading files fails, THE Agent_Module SHALL print an error message and continue processing other files
5. WHEN results are collected, THE Agent_Module SHALL return a random sample of up to 5 tips

### Requirement 11: User Interface Styling

**User Story:** As a user, I want a modern, visually appealing interface with smooth animations, so that the application is engaging and pleasant to use.

#### Acceptance Criteria

1. WHEN the application loads, THE UI_Component SHALL apply fade-in animations to the main container
2. WHEN displaying metric cards, THE UI_Component SHALL apply hover effects with transform, scale, and shadow transitions
3. WHEN displaying the header, THE UI_Component SHALL use a gradient color scheme (green tones) with text shadow
4. WHEN displaying buttons, THE UI_Component SHALL apply gradient backgrounds and scale effects on hover
5. WHEN the user hovers over input fields, THE UI_Component SHALL apply transform and shadow effects with smooth transitions

### Requirement 12: Quick Fix Recommendations

**User Story:** As a user, I want to see immediate quick-fix suggestions for my highest emission source, so that I can take action right away.

#### Acceptance Criteria

1. WHEN the highest source is electricity, THE UI_Component SHALL display a warning suggesting "Switch to LED bulbs"
2. WHEN the highest source is transport, THE UI_Component SHALL display a warning suggesting "Carpool or Walk"
3. WHEN the highest source is food, THE UI_Component SHALL display a warning suggesting "Meat-free Mondays"
4. WHEN the highest source is waste, THE UI_Component SHALL display a warning suggesting "Recycle plastics"
5. WHEN the highest source is water, THE UI_Component SHALL display a warning suggesting "Fix leaks"

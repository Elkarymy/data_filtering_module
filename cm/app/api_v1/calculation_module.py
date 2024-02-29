import pandas as pd
import os
def filter_data(df, field_of_intervention=None, intervention_type=None, space_filter=None):
    filtered_df = df.copy()  # Make a copy of the original DataFrame

    # Apply filters based on user input
    if field_of_intervention:
        filtered_df = filtered_df[filtered_df['Field_of_intervention'].str.lower() == field_of_intervention.lower()]
    if intervention_type:
        filtered_df = filtered_df[filtered_df['Type_of_intervention'].str.lower() == intervention_type.lower()]
    if space_filter:
        for col in ['Residential', 'Office', 'Educational', 'Other']:
            if space_filter.get(col) == 'Y':
                filtered_df = filtered_df[filtered_df[col].str.lower() == 'y']

    return filtered_df
def main():
    # Get the current directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV data file
    csv_file_path = os.path.join(script_dir, 'my_calculation_module_directory', 'input_data', 'cleaned_data.csv')

    print("CSV file path:", csv_file_path)  # For debugging
    if not os.path.exists(csv_file_path):
        print("Error: CSV file not found.")
        return

    print("--- Behavioural interventions ---")
    print("Please provide the following information:")

    # Prompt user for input
    field_of_intervention = input("Enter field of intervention (e.g., Occupant presence, Equipment use..): ")
    intervention_type = input(
        "Enter intervention type (e.g., Monetary incentives, Providing feedback and information...): ")
    # Prompt user for space filtering options
    print("\nSpaces to Include:")
    space_filter_options = {}
    for space_type in ['Residential', 'Office', 'Educational', 'Other']:
        choice = input(f"Include {space_type} (Y/N): ").strip().upper()
        space_filter_options[space_type] = choice
    # Read the data from CSV
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return

    # Filter the data
    filtered_data = filter_data(df, field_of_intervention=field_of_intervention, intervention_type=intervention_type,
                                space_filter=space_filter_options)

    # Display filtered data
    print("\nFiltered Data:")
    if filtered_data.empty:
        print("No data found matching the specified criteria.")
    else:
        print("-" * 100)
        print(filtered_data.to_string(index=False))
        print("-" * 100)

        # Save filtered data to CSV
        save_option = input("\nDo you want to save the filtered data to a CSV file? (Y/N): ").strip().upper()
        if save_option == 'Y':
            filename = input("Enter the filename to save the data (e.g., filtered_data): ").strip()
            filename += ".csv" if not filename.endswith(".csv") else ""  # Ensure the filename ends with .csv
            filtered_data.to_csv(filename, index=False)
            print(f"Filtered data saved to {filename}")


if __name__ == "__main__":
    main()
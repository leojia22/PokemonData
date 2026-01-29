#!/usr/bin/env python3
"""
Pokemon Tournament Data Parser - Multi-line Format
Handles data where each player's information spans multiple lines
"""

import csv
import re
import sys


def parse_record(record_str):
    """Parse record string like '15 - 2 - 1' into wins, losses, ties"""
    if not record_str or record_str.strip() == '':
        return (0, 0, 0, '')
    
    # Handle special cases like "7 - 5 - 0 drop"
    record_str_clean = record_str.replace(' drop', '').strip()
    
    parts = re.findall(r'\d+', record_str_clean)
    if len(parts) >= 3:
        wins, losses, ties = int(parts[0]), int(parts[1]), int(parts[2])
        return (wins, losses, ties, record_str)
    elif len(parts) == 2:
        wins, losses = int(parts[0]), int(parts[1])
        return (wins, losses, 0, record_str)
    else:
        return (0, 0, 0, record_str)


def parse_percentage(pct_str):
    """Parse percentage string like '59.82%' to float"""
    if not pct_str or pct_str.strip() == '':
        return ''
    pct_str = pct_str.replace('%', '').strip()
    try:
        return float(pct_str)
    except ValueError:
        return ''


def parse_multiline_format(lines):
    """
    Parse tournament data where each entry spans multiple lines:
    Line 1: Placement
    Line 2: Name
    Line 3: Country
    Line 4: Points, Record, OPW%, OOPW%
    Line 5: Deck
    (Plus blank lines between entries)
    """
    entries = []
    i = 0
    
    # Skip header
    while i < len(lines) and 'Name' not in lines[i]:
        i += 1
    i += 1  # Skip header line
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Skip marker lines
        if 'Top Cut end' in line or 'Day 2 end' in line:
            i += 1
            continue
        
        # Try to parse as placement number
        if re.match(r'^\d+$', line):
            placement = line
            
            # Get next non-empty line (name)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            name = lines[i].strip()
            
            # Get next non-empty line (country)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            country = lines[i].strip()
            
            # Get next non-empty line (points, record, percentages)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            stats_line = lines[i].strip()
            
            # Get next non-empty line (deck)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                deck = ''
            else:
                deck = lines[i].strip()
            
            # Parse stats line (points, record, opw%, oopw%)
            # Split by tabs or multiple spaces
            stats_parts = re.split(r'\t+|\s{2,}', stats_line)
            stats_parts = [p.strip() for p in stats_parts if p.strip()]
            
            if len(stats_parts) >= 4:
                points = stats_parts[0]
                record = stats_parts[1]
                opw_pct = stats_parts[2]
                oopw_pct = stats_parts[3]
                
                # Parse record
                wins, losses, ties, original_record = parse_record(record)
                
                # Parse percentages
                opw_pct_val = parse_percentage(opw_pct)
                oopw_pct_val = parse_percentage(oopw_pct)
                
                entry = {
                    'Placement': placement,
                    'Name': name,
                    'Country': country,
                    'Points': points,
                    'Wins': wins,
                    'Losses': losses,
                    'Ties': ties,
                    'Record': original_record,
                    'OPW_Percent': opw_pct_val,
                    'OOPW_Percent': oopw_pct_val,
                    'Deck': deck
                }
                
                entries.append(entry)
        
        i += 1
    
    return entries


def write_csv(entries, output_file):
    """Write entries to CSV file"""
    fieldnames = ['Placement', 'Name', 'Country', 'Points', 'Wins', 'Losses', 
                 'Ties', 'Record', 'OPW_Percent', 'OOPW_Percent', 'Deck']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Pokemon Tournament Data Parser - Multi-line Format")
        print("\nUsage:")
        print("  python pokemon_parser_multiline.py <input_file> [output_file]")
        print("\nExample:")
        print("  python pokemon_parser_multiline.py tournament.txt results.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'pokemon_tournament_data.csv'
    
    try:
        print(f"📊 Reading file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📝 Processing {len(lines)} lines...")
        entries = parse_multiline_format(lines)
        
        if entries:
            write_csv(entries, output_file)
            print(f"\n✅ SUCCESS!")
            print(f"✓ Parsed {len(entries)} tournament entries")
            print(f"✓ CSV file created: {output_file}")
            print(f"\n📈 Data summary:")
            print(f"  • Total players: {len(entries)}")
            if entries:
                print(f"  • Winner: {entries[0]['Name']} ({entries[0]['Country']})")
                print(f"  • Record: {entries[0]['Record']}")
                print(f"  • Deck: {entries[0]['Deck']}")
            print(f"\n✓ Ready for data analytics!")
        else:
            print("\n✗ No valid entries found in the input file")
            print("   Check that the file format matches the expected structure")
            
    except FileNotFoundError:
        print(f"✗ Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
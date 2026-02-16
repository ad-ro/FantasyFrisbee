#!/usr/bin/env python3
"""
Scrape PDGA Tournament by Event ID
Quick script to fetch tournament results directly by event ID
"""

import sys
import json
from tournament_parser import scrape_tournament_by_event_id, TournamentSchedule, scrape_all_with_event_ids


def scrape_single_event(event_id: str):
    """Scrape a single tournament by event ID"""
    print(f"\n{'='*80}")
    print(f"SCRAPING SINGLE TOURNAMENT")
    print(f"{'='*80}")
    
    tournament = scrape_tournament_by_event_id(event_id)
    
    if tournament:
        # Display results
        print(f"\n{'='*80}")
        print(f"RESULTS SUMMARY")
        print(f"{'='*80}")
        print(f"Tournament: {tournament['name']}")
        print(f"Event ID: {tournament['id']}")
        print(f"Division: {tournament['division']}")
        print(f"Total Players: {len(tournament['results'])}")
        
        # Show top 10
        print(f"\nTOP 10 FINISHERS:")
        print(f"{'='*80}")
        for result in tournament['results'][:10]:
            tied = "T" if result.get('tied') else " "
            print(f"{tied}{result['placement']:2d}. {result['name']:30s} PDGA #{result['pdga_number']}")
        
        # Save to file
        output_file = f"event_{event_id}_results.json"
        with open(output_file, 'w') as f:
            json.dump(tournament, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"✅ Results saved to: {output_file}")
        print(f"{'='*80}\n")
        
        return True
    else:
        print(f"\n❌ Failed to scrape event {event_id}")
        return False


def scrape_schedule_events():
    """Scrape all tournaments with event IDs from the schedule"""
    print(f"\n{'='*80}")
    print(f"SCRAPING SCHEDULED TOURNAMENTS")
    print(f"{'='*80}")
    
    schedule = TournamentSchedule()
    
    if not schedule.tournaments:
        print("\n❌ No tournaments loaded from schedule")
        return False
    
    # Show what we'll scrape
    with_ids = schedule.get_tournaments_with_event_ids()
    
    if not with_ids:
        print("\n⚠️  No tournaments with event IDs in schedule")
        print("\nTo add event IDs:")
        print("1. Edit tournaments.txt")
        print("2. Format: Name,Tier,Dates,EventID")
        print("3. Example: Supreme Flight Open,ES,February 27 - March 1,88276")
        return False
    
    print(f"\nFound {len(with_ids)} tournaments with event IDs:")
    for t in with_ids:
        print(f"  • {t['name']} (ID: {t['event_id']})")
    
    # Ask for confirmation
    response = input(f"\nScrape all {len(with_ids)} tournaments? (y/n): ")
    
    if response.lower() != 'y':
        print("Cancelled")
        return False
    
    # Scrape all
    results = scrape_all_with_event_ids(schedule)
    
    if results:
        # Save combined results
        output_file = "all_tournament_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"✅ All results saved to: {output_file}")
        print(f"{'='*80}\n")
        
        return True
    else:
        print("\n❌ No results scraped")
        return False


def interactive_mode():
    """Interactive mode for scraping"""
    print(f"\n{'='*80}")
    print(f"PDGA TOURNAMENT SCRAPER")
    print(f"{'='*80}")
    
    print("\nOptions:")
    print("  1. Scrape by event ID")
    print("  2. Scrape all tournaments with IDs from schedule")
    print("  3. Show schedule")
    print("  4. Exit")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        event_id = input("Enter PDGA event ID: ")
        scrape_single_event(event_id)
    
    elif choice == '2':
        scrape_schedule_events()
    
    elif choice == '3':
        schedule = TournamentSchedule()
        schedule.print_schedule()
    
    elif choice == '4':
        print("Goodbye!")
        return
    
    else:
        print("Invalid option")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("\nUsage:")
            print(f"  {sys.argv[0]}                  Interactive mode")
            print(f"  {sys.argv[0]} EVENT_ID         Scrape specific event")
            print(f"  {sys.argv[0]} --all           Scrape all scheduled events with IDs")
            print(f"  {sys.argv[0]} --schedule      Show tournament schedule")
            print("\nExamples:")
            print(f"  {sys.argv[0]} 88276           Scrape Supreme Flight Open")
            print(f"  {sys.argv[0]} --all           Scrape all scheduled tournaments")
            print()
        
        elif sys.argv[1] == '--all':
            scrape_schedule_events()
        
        elif sys.argv[1] == '--schedule':
            schedule = TournamentSchedule()
            schedule.print_schedule()
        
        elif sys.argv[1].isdigit():
            # Event ID provided
            scrape_single_event(sys.argv[1])
        
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print(f"Use --help for usage information")
    
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()

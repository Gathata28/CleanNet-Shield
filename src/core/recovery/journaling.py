#!/usr/bin/env python3
"""
Journaling module for recovery tracking and emotional support
"""

import os
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

# Handle imports for both standalone and package usage
try:
    from src.utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from utils.logger import Logger


class Journal:
    def __init__(self):
        """Initialize the journaling system"""
        self.logger = Logger()

        # Data directory
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "journal"
        )
        os.makedirs(self.data_dir, exist_ok=True)

        # Journal file (one per month)
        self.current_month = datetime.now().strftime("%Y-%m")
        self.journal_file = os.path.join(
            self.data_dir, f"journal_{self.current_month}.json"
        )

        # Mood and trigger tracking
        self.moods = ["Excellent", "Good", "Okay", "Struggling", "Difficult"]

        self.common_triggers = [
            "Stress",
            "Boredom",
            "Loneliness",
            "Anxiety",
            "Anger",
            "Sadness",
            "Tiredness",
            "Social Media",
            "Internet Browsing",
            "Work Pressure",
            "Relationship Issues",
            "Other",
        ]

        self.coping_strategies = [
            "Exercise",
            "Meditation",
            "Talking to Someone",
            "Journaling",
            "Reading",
            "Music",
            "Hobbies",
            "Outdoor Activities",
            "Breathing Exercises",
            "Cold Shower",
            "Other",
        ]

        self.logger.debug("Journal system initialized")

    def _load_journal_data(self) -> Dict:
        """Load journal data for current month"""
        try:
            if os.path.exists(self.journal_file):
                with open(self.journal_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load journal data: {e}")
            return {}

    def _save_journal_data(self, data: Dict):
        """Save journal data"""
        try:
            with open(self.journal_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save journal data: {e}")

    def add_entry(
        self,
        content: str,
        mood: Optional[str] = None,
        triggers: Optional[List[str]] = None,
        coping_used: Optional[List[str]] = None,
        rating: Optional[int] = None,
    ) -> bool:
        """
        Add a journal entry for today

        Args:
            content: Main journal text
            mood: Current mood (from predefined list)
            triggers: List of triggers experienced
            coping_used: List of coping strategies used
            rating: Overall day rating (1-10)

        Returns:
            True if entry was saved successfully
        """
        try:
            today = date.today().isoformat()

            # Load existing data
            journal_data = self._load_journal_data()

            # Create entry
            entry = {
                "date": today,
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "mood": mood,
                "triggers": triggers or [],
                "coping_used": coping_used or [],
                "rating": rating,
                "word_count": len(content.split()),
                "character_count": len(content),
            }

            # Save entry (overwrites existing entry for today)
            journal_data[today] = entry

            self._save_journal_data(journal_data)

            self.logger.log_recovery_action(
                "journal_entry_added",
                {
                    "date": today,
                    "word_count": entry["word_count"],
                    "mood": mood,
                    "rating": rating,
                },
            )

            self.logger.info(f"Journal entry added for {today}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add journal entry: {e}")
            return False

    def get_entry(self, entry_date: Optional[date] = None) -> Optional[Dict]:
        """
        Get journal entry for a specific date

        Args:
            entry_date: Date to get entry for. If None, gets today's entry

        Returns:
            Journal entry dictionary or None if not found
        """
        try:
            if entry_date is None:
                entry_date = date.today()

            date_str = entry_date.isoformat()

            # Check if we need to load a different month's file
            month_str = entry_date.strftime("%Y-%m")
            if month_str != self.current_month:
                journal_file = os.path.join(self.data_dir, f"journal_{month_str}.json")
                if os.path.exists(journal_file):
                    with open(journal_file, "r", encoding="utf-8") as f:
                        journal_data = json.load(f)
                else:
                    return None
            else:
                journal_data = self._load_journal_data()

            return journal_data.get(date_str)

        except Exception as e:
            self.logger.error(f"Failed to get journal entry for {entry_date}: {e}")
            return None

    def get_todays_entry(self) -> Optional[str]:
        """
        Get today's journal entry content

        Returns:
            Today's journal content or None if no entry exists
        """
        entry = self.get_entry()
        return entry["content"] if entry else None

    def update_mood_and_triggers(
        self, mood: str, triggers: List[str], coping_used: List[str], rating: int
    ) -> bool:
        """
        Update mood, triggers, and coping strategies for today's entry

        Args:
            mood: Current mood
            triggers: List of triggers
            coping_used: List of coping strategies used
            rating: Day rating (1-10)

        Returns:
            True if update was successful
        """
        try:
            today = date.today().isoformat()
            journal_data = self._load_journal_data()

            if today in journal_data:
                # Update existing entry
                entry = journal_data[today]
                entry["mood"] = mood
                entry["triggers"] = triggers
                entry["coping_used"] = coping_used
                entry["rating"] = rating
                entry["last_updated"] = datetime.now().isoformat()
            else:
                # Create new entry with just mood/trigger data
                entry = {
                    "date": today,
                    "timestamp": datetime.now().isoformat(),
                    "content": "",
                    "mood": mood,
                    "triggers": triggers,
                    "coping_used": coping_used,
                    "rating": rating,
                }
                journal_data[today] = entry

            self._save_journal_data(journal_data)

            self.logger.log_recovery_action(
                "mood_triggers_updated",
                {
                    "date": today,
                    "mood": mood,
                    "triggers_count": len(triggers),
                    "coping_count": len(coping_used),
                    "rating": rating,
                },
            )

            return True

        except Exception as e:
            self.logger.error(f"Failed to update mood and triggers: {e}")
            return False

    def get_recent_entries(self, days: int = 7) -> List[Dict]:
        """
        Get recent journal entries

        Args:
            days: Number of recent days to retrieve

        Returns:
            List of journal entries, newest first
        """
        try:
            entries = []
            current_date = date.today()

            for i in range(days):
                entry_date = current_date - timedelta(days=i)
                entry = self.get_entry(entry_date)
                if entry:
                    entries.append(entry)

            return entries

        except Exception as e:
            self.logger.error(f"Failed to get recent entries: {e}")
            return []

    def get_monthly_summary(self, month: Optional[str] = None) -> Dict:
        """
        Get summary statistics for a month

        Args:
            month: Month in YYYY-MM format. If None, uses current month

        Returns:
            Dictionary with monthly statistics
        """
        try:
            if month is None:
                month = self.current_month

            journal_file = os.path.join(self.data_dir, f"journal_{month}.json")

            if not os.path.exists(journal_file):
                return {"month": month, "entries_count": 0}

            with open(journal_file, "r", encoding="utf-8") as f:
                journal_data = json.load(f)

            entries = list(journal_data.values())

            # Calculate statistics
            stats = {
                "month": month,
                "entries_count": len(entries),
                "total_words": sum(entry.get("word_count", 0) for entry in entries),
                "average_rating": 0,
                "mood_distribution": {},
                "common_triggers": {},
                "effective_coping": {},
                "best_days": [],
                "challenging_days": [],
            }

            if entries:
                # Average rating
                ratings = [
                    entry.get("rating") for entry in entries if entry.get("rating")
                ]
                if ratings:
                    stats["average_rating"] = round(sum(ratings) / len(ratings), 1)

                # Mood distribution
                moods = [entry.get("mood") for entry in entries if entry.get("mood")]
                for mood in moods:
                    stats["mood_distribution"][mood] = (
                        stats["mood_distribution"].get(mood, 0) + 1
                    )

                # Common triggers
                all_triggers = []
                for entry in entries:
                    all_triggers.extend(entry.get("triggers", []))
                for trigger in all_triggers:
                    stats["common_triggers"][trigger] = (
                        stats["common_triggers"].get(trigger, 0) + 1
                    )

                # Effective coping strategies
                all_coping = []
                for entry in entries:
                    all_coping.extend(entry.get("coping_used", []))
                for coping in all_coping:
                    stats["effective_coping"][coping] = (
                        stats["effective_coping"].get(coping, 0) + 1
                    )

                # Best and challenging days
                rated_entries = [
                    (entry["date"], entry["rating"])
                    for entry in entries
                    if entry.get("rating")
                ]
                if rated_entries:
                    sorted_entries = sorted(
                        rated_entries, key=lambda x: x[1], reverse=True
                    )
                    stats["best_days"] = sorted_entries[:3]  # Top 3
                    stats["challenging_days"] = sorted_entries[-3:]  # Bottom 3

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get monthly summary: {e}")
            return {"month": month, "error": str(e)}

    def search_entries(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        Search journal entries for a keyword

        Args:
            keyword: Keyword to search for
            max_results: Maximum number of results to return

        Returns:
            List of matching entries
        """
        try:
            matches = []
            keyword_lower = keyword.lower()

            # Search in current month
            journal_data = self._load_journal_data()
            for entry in journal_data.values():
                content = entry.get("content", "").lower()
                if keyword_lower in content:
                    matches.append(entry)

            # Search in previous months (last 6 months)
            current_date = datetime.now()
            for i in range(1, 7):
                try:
                    search_date = current_date.replace(month=current_date.month - i)
                    month_str = search_date.strftime("%Y-%m")
                    journal_file = os.path.join(
                        self.data_dir, f"journal_{month_str}.json"
                    )

                    if os.path.exists(journal_file):
                        with open(journal_file, "r", encoding="utf-8") as f:
                            month_data = json.load(f)

                        for entry in month_data.values():
                            content = entry.get("content", "").lower()
                            if keyword_lower in content:
                                matches.append(entry)
                except Exception:
                    continue

            # Sort by date (newest first) and limit results
            matches.sort(key=lambda x: x.get("date", ""), reverse=True)
            return matches[:max_results]

        except Exception as e:
            self.logger.error(f"Failed to search entries: {e}")
            return []

    def export_journal(
        self,
        output_path: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> bool:
        """
        Export journal entries to a text file

        Args:
            output_path: Path to save the exported journal
            start_date: Start date for export (inclusive)
            end_date: End date for export (inclusive)

        Returns:
            True if export was successful
        """
        try:
            if start_date is None:
                # Start of current month
                start_date = date.today().replace(day=1)
            if end_date is None:
                # End date is today
                end_date = date.today()

            # Collect entries in date range
            entries = []
            current_date = start_date
            while current_date <= end_date:
                entry = self.get_entry(current_date)
                if entry:
                    entries.append(entry)
                current_date += timedelta(days=1)

            # Write to file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("Journal Export\n")
                f.write(f"Date Range: {start_date} to {end_date}\n")
                f.write(f"Total Entries: {len(entries)}\n")
                f.write("=" * 50 + "\n\n")

                for entry in entries:
                    f.write(f"Date: {entry['date']}\n")
                    if entry.get("mood"):
                        f.write(f"Mood: {entry['mood']}\n")
                    if entry.get("rating"):
                        f.write(f"Rating: {entry['rating']}/10\n")
                    if entry.get("triggers"):
                        f.write(f"Triggers: {', '.join(entry['triggers'])}\n")
                    if entry.get("coping_used"):
                        f.write(
                            f"Coping Strategies: {', '.join(entry['coping_used'])}\n"
                        )
                    f.write("\n")
                    f.write(entry.get("content", ""))
                    f.write("\n" + "-" * 30 + "\n\n")

            self.logger.info(
                f"Journal exported to {output_path}: " f"{len(entries)} entries"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to export journal: {e}")
            return False

    def get_available_months(self) -> List[str]:
        """
        Get list of months that have journal data

        Returns:
            List of month strings in YYYY-MM format
        """
        try:
            months = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith("journal_") and filename.endswith(".json"):
                    month = filename[8:-5]  # Extract YYYY-MM from journal_YYYY-MM.json
                    months.append(month)

            return sorted(months, reverse=True)  # Newest first

        except Exception as e:
            self.logger.error(f"Failed to get available months: {e}")
            return []


if __name__ == "__main__":
    # Test the journal system
    journal = Journal()

    # Add test entry
    success = journal.add_entry(
        "Today was a challenging day, but I managed to resist urges by "
        "going for a walk.",
        mood="Okay",
        triggers=["Stress", "Boredom"],
        coping_used=["Exercise", "Breathing Exercises"],
        rating=6,
    )
    print(f"Entry added: {success}")

    # Get today's entry
    today_entry = journal.get_todays_entry()
    print(f"Today's entry: {today_entry}")

    # Get monthly summary
    summary = journal.get_monthly_summary()
    print(f"Monthly summary: {summary}")

    # Get available months
    months = journal.get_available_months()
    print(f"Available months: {months}")

#!/usr/bin/env python3
"""
Accountability bot module for recovery support and notifications
"""

import json
import os
import random
import smtplib
import requests
from email.mime.text import MIMEText
from typing import Dict

# Handle imports for both standalone and package usage
try:
    from src.utils.logger import Logger
except ImportError:
    # Fallback for standalone usage
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from utils.logger import Logger


class AccountabilityBot:
    def __init__(self):
        """Initialize the accountability bot"""
        self.logger = Logger()

        # Data directory
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "accountability"
        )
        os.makedirs(self.data_dir, exist_ok=True)

        # Configuration file
        self.config_file = os.path.join(self.data_dir, "accountability_config.json")

        # Default configuration
        self.default_config = {
            "email_enabled": False,
            "email_settings": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",  # Use app password for Gmail
                "from_email": "",
                "to_emails": [],
            },
            "telegram_enabled": False,
            "telegram_settings": {"bot_token": "", "chat_ids": []},
            "notification_schedule": {
                "daily_checkin": True,
                "checkin_time": "20:00",  # 8 PM
                "weekly_report": True,
                "report_day": "sunday",
                "milestone_alerts": True,
                "emergency_support": True,
            },
            "motivation_messages": [
                "Remember why you started this journey. "
                "You're stronger than your urges!",
                "Every moment of resistance makes you stronger. Keep going!",
                "Your future self is counting on the choices you make today.",
                "Recovery is a process, not an event. Be patient with yourself.",
                "You've overcome challenges before, and you can do it again.",
                "Focus on progress, not perfection. Every day clean is a victory!",
                "Your brain is healing. Give it time and be kind to yourself.",
                "Seek support when you need it. You don't have to do this alone.",
                "Remember: This urge will pass. You have the power to choose.",
                "One day at a time. You've got this!",
            ],
            "emergency_resources": [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "SAMHSA National Helpline: 1-800-662-4357",
                "Sex Addicts Anonymous: https://saa-recovery.org/",
                "NoFap Community: https://nofap.com/",
                "Fight The New Drug: https://fightthenewdrug.org/",
            ],
        }

        # Load configuration
        self.config = self._load_config()

        self.logger.debug("Accountability bot initialized")

    def _load_config(self) -> Dict:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                # Merge with defaults
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            else:
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            self.logger.error(f"Failed to load accountability config: {e}")
            return self.default_config

    def _save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save accountability config: {e}")

    def set_email(
        self,
        email: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        username: str = "",
        password: str = "",
    ) -> bool:
        """
        Configure email settings for notifications

        Args:
            email: Email address to send notifications to
            smtp_server: SMTP server (default: Gmail)
            smtp_port: SMTP port (default: 587)
            username: SMTP username (usually your email)
            password: SMTP password (use app password for Gmail)

        Returns:
            True if configuration was saved successfully
        """
        try:
            self.config["email_enabled"] = True
            self.config["email_settings"].update(
                {
                    "smtp_server": smtp_server,
                    "smtp_port": smtp_port,
                    "username": username or email,
                    "password": password,
                    "from_email": username or email,
                    "to_emails": (
                        [email]
                        if email not in self.config["email_settings"]["to_emails"]
                        else self.config["email_settings"]["to_emails"]
                    ),
                }
            )

            if email not in self.config["email_settings"]["to_emails"]:
                self.config["email_settings"]["to_emails"].append(email)

            self._save_config(self.config)
            self.logger.info(f"Email accountability configured for: {email}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to set email configuration: {e}")
            return False

    def set_telegram(self, bot_token: str, chat_id: str) -> bool:
        """
        Configure Telegram bot settings

        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to

        Returns:
            True if configuration was saved successfully
        """
        try:
            self.config["telegram_enabled"] = True
            self.config["telegram_settings"]["bot_token"] = bot_token

            if chat_id not in self.config["telegram_settings"]["chat_ids"]:
                self.config["telegram_settings"]["chat_ids"].append(chat_id)

            self._save_config(self.config)
            self.logger.info(f"Telegram accountability configured for chat: {chat_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to set Telegram configuration: {e}")
            return False

    def send_email(
        self, subject: str, message: str, is_emergency: bool = False
    ) -> bool:
        """
        Send email notification

        Args:
            subject: Email subject
            message: Email message body
            is_emergency: Whether this is an emergency message

        Returns:
            True if email was sent successfully
        """
        if not self.config["email_enabled"]:
            self.logger.warning("Email not configured, cannot send notification")
            return False

        try:
            email_settings = self.config["email_settings"]

            # Create message
            msg = MIMEText(message, "plain")
            msg["From"] = email_settings["from_email"]
            msg["Subject"] = (
                f"{'🚨 URGENT - ' if is_emergency else ''}"
                f"Adult Content Blocker: {subject}"
            )

            # Send to all configured emails
            smtp_server = smtplib.SMTP(
                email_settings["smtp_server"], email_settings["smtp_port"]
            )
            smtp_server.starttls()
            smtp_server.login(email_settings["username"], email_settings["password"])

            for to_email in email_settings["to_emails"]:
                msg["To"] = to_email
                smtp_server.send_message(msg)
                self.logger.info(f"Accountability email sent to: {to_email}")

            smtp_server.quit()

            self.logger.log_recovery_action(
                "email_sent",
                {
                    "subject": subject,
                    "recipients": len(email_settings["to_emails"]),
                    "is_emergency": is_emergency,
                },
            )

            self.logger.info(
                f"Successfully sent email notification to "
                f"{len(email_settings['to_emails'])} recipients"
            )

            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def send_telegram_message(self, message: str, is_emergency: bool = False) -> bool:
        """
        Send Telegram message

        Args:
            message: Message to send
            is_emergency: Whether this is an emergency message

        Returns:
            True if message was sent successfully
        """
        if not self.config["telegram_enabled"]:
            self.logger.warning("Telegram not configured, cannot send notification")
            return False

        try:
            telegram_settings = self.config["telegram_settings"]
            bot_token = telegram_settings["bot_token"]

            # Build message
            full_message = (
                f"{'🚨 URGENT 🚨\\n\\n' if is_emergency else ''}"
                f"🛡️ Adult Content Blocker\\n\\n{message}"
            )

            if is_emergency:
                full_message += "\\n\\n🆘 Emergency Resources:\\n"
                for resource in self.config["emergency_resources"][
                    :3
                ]:  # First 3 resources
                    full_message += f"• {resource}\\n"

            # Send to all configured chat IDs
            success_count = 0
            for chat_id in telegram_settings["chat_ids"]:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": full_message,
                    "parse_mode": "Markdown" if not is_emergency else None,
                }

                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    success_count += 1
                    self.logger.info(f"Telegram message sent to chat: {chat_id}")
                else:
                    self.logger.error(
                        f"Failed to send Telegram message to {chat_id}: {response.text}"
                    )

            if success_count > 0:
                self.logger.log_recovery_action(
                    "telegram_sent",
                    {"recipients": success_count, "is_emergency": is_emergency},
                )
                self.logger.info(
                    f"Successfully sent Telegram notification to "
                    f"{len(telegram_settings['chat_ids'])} recipients"
                )
                return True
            else:
                return False

        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_motivation_message(self) -> bool:
        """Send a random motivation message"""
        try:
            message = random.choice(self.config["motivation_messages"])

            subject = "Daily Motivation"
            full_message = f"💪 Your daily motivation:\\n\\n{message}\\n\\nKeep up the great work on your recovery journey!"

            # Send via email and/or Telegram
            email_sent = (
                self.send_email(subject, full_message)
                if self.config["email_enabled"]
                else True
            )
            telegram_sent = (
                self.send_telegram_message(full_message)
                if self.config["telegram_enabled"]
                else True
            )

            self.logger.info(
                f"Successfully sent motivation message to "
                f"{len(self.config['telegram_settings']['chat_ids'])} recipients"
            )

            return email_sent or telegram_sent

        except Exception as e:
            self.logger.error(f"Failed to send motivation message: {e}")
            return False

    def send_streak_milestone_alert(
        self, streak_days: int, milestone_message: str
    ) -> bool:
        """
        Send notification for streak milestone

        Args:
            streak_days: Number of days in current streak
            milestone_message: Achievement message

        Returns:
            True if notification was sent successfully
        """
        try:
            subject = f"Milestone Achieved: {streak_days} Days!"
            message = f"""
🎉 CONGRATULATIONS! 🎉

{milestone_message}

You've reached {streak_days} consecutive clean days! This is a significant achievement in your recovery journey.

Keep building on this momentum. You're proving to yourself that you have the strength and determination to overcome challenges.

Your commitment to change is inspiring!

Stay strong! 💪
"""

            # Send via email and/or Telegram
            email_sent = (
                self.send_email(subject, message)
                if self.config["email_enabled"]
                else True
            )
            telegram_sent = (
                self.send_telegram_message(message)
                if self.config["telegram_enabled"]
                else True
            )

            self.logger.info(
                f"Successfully sent streak milestone alert to "
                f"{len(self.config['telegram_settings']['chat_ids'])} recipients"
            )

            return email_sent or telegram_sent

        except Exception as e:
            self.logger.error(f"Failed to send milestone alert: {e}")
            return False

    def send_emergency_support(self, trigger_type: str = "unknown") -> bool:
        """
        Send emergency support message with resources

        Args:
            trigger_type: Type of trigger or situation

        Returns:
            True if message was sent successfully
        """
        try:
            subject = "Emergency Support Needed"
            message = f"""
🚨 URGENT SUPPORT REQUEST 🚨

It looks like you're facing a challenging moment in your recovery. Remember:

1. This feeling WILL pass
2. You have overcome urges before
3. Reaching out for help shows strength, not weakness

IMMEDIATE ACTIONS YOU CAN TAKE:
• Take 10 deep breaths
• Go for a walk or do physical exercise
• Call a friend or family member
• Use a coping strategy from your toolkit
• Remember your reasons for recovery

If trigger type: {trigger_type}

You are stronger than this moment. Your future self is counting on the choice you make right now.
"""

            # Send via email and/or Telegram (marked as emergency)
            email_sent = (
                self.send_email(subject, message, is_emergency=True)
                if self.config["email_enabled"]
                else True
            )
            telegram_sent = (
                self.send_telegram_message(message, is_emergency=True)
                if self.config["telegram_enabled"]
                else True
            )

            self.logger.info(
                f"Successfully sent emergency support message to "
                f"{len(self.config['telegram_settings']['chat_ids'])} recipients"
            )

            return email_sent or telegram_sent

        except Exception as e:
            self.logger.error(f"Failed to send emergency support: {e}")
            return False

    def send_weekly_report(self, streak_data: Dict, journal_summary: Dict) -> bool:
        """
        Send weekly progress report

        Args:
            streak_data: Streak tracking data
            journal_summary: Journal summary data

        Returns:
            True if report was sent successfully
        """
        try:
            current_streak = streak_data.get("current_streak", 0)
            longest_streak = streak_data.get("longest_streak", 0)
            total_clean_days = streak_data.get("total_clean_days", 0)

            subject = f"Weekly Report - {current_streak} Day Streak"
            message = f"""
📊 WEEKLY RECOVERY REPORT

STREAK PROGRESS:
• Current Streak: {current_streak} days
• Longest Streak: {longest_streak} days
• Total Clean Days: {total_clean_days} days

JOURNAL ACTIVITY:
• Entries This Week: {journal_summary.get('entries_count', 0)}
• Average Mood: {journal_summary.get('average_mood', 'N/A')}
• Most Common Trigger: {journal_summary.get('top_trigger', 'N/A')}

ACHIEVEMENTS:
• Achievements Unlocked: {streak_data.get('achievements_count', 0)}

MOTIVATION FOR NEXT WEEK:
Remember that recovery is a journey, not a destination. Every day you choose recovery, you're building a stronger, healthier version of yourself.

Keep up the excellent work! 💪

---
Stay committed to your goals and remember why you started this journey.
"""

            # Send via email and/or Telegram
            email_sent = (
                self.send_email(subject, message)
                if self.config["email_enabled"]
                else True
            )
            telegram_sent = (
                self.send_telegram_message(message)
                if self.config["telegram_enabled"]
                else True
            )

            self.logger.info(
                f"Successfully sent weekly report to "
                f"{len(self.config['telegram_settings']['chat_ids'])} recipients"
            )

            return email_sent or telegram_sent

        except Exception as e:
            self.logger.error(f"Failed to send weekly report: {e}")
            return False

    def send_test_email(self) -> bool:
        """Send a test email to verify configuration"""
        return self.send_email(
            "Test Message",
            "This is a test message from your Adult Content Blocker accountability system. If you received this, your email notifications are working correctly!",
        )

    def send_test_telegram(self) -> bool:
        """Send a test Telegram message to verify configuration"""
        return self.send_telegram_message(
            "This is a test message from your Adult Content Blocker accountability system. If you received this, your Telegram notifications are working correctly!"
        )

    def schedule_daily_checkin(self) -> bool:
        """
        Schedule or trigger daily check-in notification
        (In a full implementation, this would integrate with a task scheduler)

        Returns:
            True if check-in was sent successfully
        """
        try:
            subject = "Daily Check-In"
            message = """
🌅 DAILY CHECK-IN

Good evening! Time for your daily recovery check-in.

REFLECTION QUESTIONS:
• How are you feeling today?
• What challenges did you face?
• What victories can you celebrate?
• What coping strategies did you use?

Consider writing in your journal about today's experiences. Every day of reflection contributes to your growth and recovery.

You've got this! Tomorrow is another opportunity to continue your journey. 🌟
"""

            # Send via email and/or Telegram
            email_sent = (
                self.send_email(subject, message)
                if self.config["email_enabled"]
                else True
            )
            telegram_sent = (
                self.send_telegram_message(message)
                if self.config["telegram_enabled"]
                else True
            )

            self.logger.info(
                f"Successfully scheduled daily checkin for "
                f"{len(self.config['telegram_settings']['chat_ids'])} recipients"
            )

            return email_sent or telegram_sent

        except Exception as e:
            self.logger.error(f"Failed to send daily check-in: {e}")
            return False

    def get_config_status(self) -> Dict:
        """Get current configuration status"""
        return {
            "email_enabled": self.config["email_enabled"],
            "email_configured": bool(self.config["email_settings"]["to_emails"]),
            "telegram_enabled": self.config["telegram_enabled"],
            "telegram_configured": bool(self.config["telegram_settings"]["chat_ids"]),
            "notification_schedule": self.config["notification_schedule"],
            "total_contacts": len(self.config["email_settings"]["to_emails"])
            + len(self.config["telegram_settings"]["chat_ids"]),
        }

    def update_notification_settings(self, settings: Dict) -> bool:
        """Update notification schedule settings"""
        try:
            self.config["notification_schedule"].update(settings)
            self._save_config(self.config)
            self.logger.info("Notification settings updated")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update notification settings: {e}")
            return False


if __name__ == "__main__":
    # Test the accountability bot
    bot = AccountabilityBot()

    print(f"Config status: {bot.get_config_status()}")

    # Uncomment to test email (need to configure first)
    bot.set_email(
        "your-email@gmail.com",
        username="your-email@gmail.com",
        password="your-app-password",
    )
    result = bot.send_test_email()
    print(f"Test email sent: {result}")

    # Test motivation message
    result = bot.send_motivation_message()
    print(f"Motivation message sent: {result}")

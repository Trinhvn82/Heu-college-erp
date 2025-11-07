"""
Django management command to check active sessions and their timeout settings
Usage: python manage.py check_sessions
"""

from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
from info.models import User
from datetime import datetime


class Command(BaseCommand):
    help = 'Check active sessions and their timeout configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Show all sessions including expired ones',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Show sessions for specific username',
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("SESSION TIMEOUT CHECKER"))
        self.stdout.write("=" * 80)
        
        # Get sessions
        if options['all']:
            sessions = Session.objects.all().order_by('-expire_date')
            self.stdout.write(f"\n📊 Showing ALL sessions\n")
        else:
            now = timezone.now()
            sessions = Session.objects.filter(expire_date__gte=now).order_by('-expire_date')
            self.stdout.write(f"\n📊 Showing ACTIVE sessions only\n")
        
        if not sessions.exists():
            self.stdout.write(self.style.WARNING("\n⚠️  No sessions found\n"))
            return
        
        self.stdout.write(f"Total sessions: {sessions.count()}\n")
        self.stdout.write("-" * 80)
        
        for i, session in enumerate(sessions, 1):
            try:
                data = session.get_decoded()
                user_id = data.get('_auth_user_id')
                
                if not user_id:
                    continue
                
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    self.stdout.write(f"\n{i}. Session (User deleted)")
                    continue
                
                # Filter by username if specified
                if options['username'] and user.username != options['username']:
                    continue
                
                # Check user type
                is_renter = hasattr(user, 'renter')
                user_type = "🏠 Renter" if is_renter else "👤 Chủ nhà/Admin"
                expected_timeout = "10 minutes" if is_renter else "30 minutes"
                
                # Calculate time info
                now = timezone.now()
                if session.expire_date > now:
                    time_left = (session.expire_date - now).total_seconds() / 60
                    status = self.style.SUCCESS("✅ ACTIVE")
                    time_info = self.style.SUCCESS(f"{time_left:.1f} minutes left")
                else:
                    time_ago = (now - session.expire_date).total_seconds() / 60
                    status = self.style.ERROR("❌ EXPIRED")
                    time_info = self.style.ERROR(f"{time_ago:.1f} minutes ago")
                
                # Display session info
                self.stdout.write(f"\n{i}. {status}")
                self.stdout.write(f"   Username: {user.username}")
                self.stdout.write(f"   User Type: {user_type}")
                self.stdout.write(f"   Expected Timeout: {expected_timeout}")
                self.stdout.write(f"   Expires: {session.expire_date.strftime('%Y-%m-%d %H:%M:%S')}")
                self.stdout.write(f"   Status: {time_info}")
                
                # Additional user info
                if is_renter:
                    renter = user.renter
                    self.stdout.write(f"   Renter Name: {renter.hoten}")
                    self.stdout.write(f"   Phone: {renter.sdt}")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n{i}. Error decoding session: {e}"))
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("\n✅ Session check complete!\n"))
        
        # Summary
        self.stdout.write("💡 Tips:")
        self.stdout.write("   - Use --all to see expired sessions")
        self.stdout.write("   - Use --username <name> to filter by user")
        self.stdout.write("   - Sessions auto-refresh on each request (SESSION_SAVE_EVERY_REQUEST=True)")
        self.stdout.write("")

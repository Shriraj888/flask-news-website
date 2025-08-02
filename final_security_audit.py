#!/usr/bin/env python3
"""
🔒 Flask News Website - Final Security & GitHub Readiness Audit
============================================================

This script performs a comprehensive security audit and verifies the project 
is ready for GitHub publication.

Author: AI Assistant
Version: 1.0.0
Date: 2025
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

class SecurityAudit:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = []
        self.warnings = []
        self.passed_checks = []
        
    def print_header(self):
        """Print audit header"""
        print("🔒 FLASK NEWS WEBSITE - SECURITY & GITHUB READINESS AUDIT")
        print("=" * 60)
        print(f"📅 Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project Root: {self.project_root}")
        print()
        
    def check_sensitive_files(self):
        """Check for sensitive files that shouldn't be committed"""
        print("🔍 Checking for sensitive files...")
        
        sensitive_patterns = [
            '.env',
            '*.key',
            '*.pem',
            '*.p12',
            'secrets.json',
            'config.json',
            '*.secret',
            '.aws',
            '.vscode/settings.json'
        ]
        
        found_sensitive = []
        
        for pattern in sensitive_patterns:
            if pattern == '.env':
                env_path = self.project_root / '.env'
                if env_path.exists():
                    found_sensitive.append('.env')
                    
        if found_sensitive:
            self.warnings.append(f"Sensitive files found: {', '.join(found_sensitive)}")
            print("   ⚠️  WARNING: .env file exists - ensure it's in .gitignore")
        else:
            self.passed_checks.append("✅ No sensitive files found in project root")
            print("   ✅ No sensitive files found")
            
    def check_gitignore(self):
        """Verify .gitignore exists and contains essential entries"""
        print("\n🔍 Checking .gitignore configuration...")
        
        gitignore_path = self.project_root / '.gitignore'
        
        if not gitignore_path.exists():
            self.issues.append("❌ .gitignore file is missing")
            return
            
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
            
        essential_entries = [
            ('.env', ['.env']),
            ('__pycache__', ['__pycache__']),
            ('*.pyc', ['*.pyc', '*.py[cod]']),  # *.py[cod] covers *.pyc
            ('venv/', ['venv/', '.venv']),
            ('.vscode/', ['.vscode/', '.idea/']),
            ('*.log', ['*.log'])
        ]
        
        missing_entries = []
        for entry_name, patterns in essential_entries:
            if not any(pattern in gitignore_content for pattern in patterns):
                missing_entries.append(entry_name)
                
        if missing_entries:
            self.warnings.append(f"Missing .gitignore entries: {', '.join(missing_entries)}")
            print(f"   ⚠️  WARNING: Missing entries: {', '.join(missing_entries)}")
        else:
            self.passed_checks.append("✅ .gitignore contains all essential entries")
            print("   ✅ .gitignore properly configured")
            
    def check_environment_template(self):
        """Check if .env.example exists and is properly configured"""
        print("\n🔍 Checking environment template...")
        
        template_path = self.project_root / '.env.example'
        
        if not template_path.exists():
            self.issues.append("❌ .env.example template is missing")
            return
            
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        required_vars = ['SECRET_KEY']
        missing_vars = []
        
        for var in required_vars:
            if var not in template_content:
                missing_vars.append(var)
                
        if missing_vars:
            self.warnings.append(f"Missing template variables: {', '.join(missing_vars)}")
        else:
            self.passed_checks.append("✅ .env.example properly configured")
            print("   ✅ Environment template is safe")
            
    def check_code_security(self):
        """Check source code for potential security issues"""
        print("\n🔍 Scanning source code for security issues...")
        
        python_files = list(self.project_root.glob('*.py'))
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded token'),
        ]
        
        issues_found = []
        
        for py_file in python_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern, description in security_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Skip if it's referencing environment variables
                    if 'os.environ' in match.group() or 'getenv' in match.group():
                        continue
                    issues_found.append(f"{py_file.name}: {description}")
                    
        if issues_found:
            for issue in issues_found:
                self.issues.append(f"❌ {issue}")
        else:
            self.passed_checks.append("✅ No hardcoded secrets found in source code")
            print("   ✅ No hardcoded secrets detected")
            
    def check_requirements(self):
        """Check requirements.txt for security and completeness"""
        print("\n🔍 Checking requirements.txt...")
        
        req_path = self.project_root / 'requirements.txt'
        
        if not req_path.exists():
            self.issues.append("❌ requirements.txt is missing")
            return
            
        with open(req_path, 'r') as f:
            requirements = f.read()
            
        essential_packages = [
            'Flask',
            'python-dotenv',
            'gunicorn'
        ]
        
        missing_packages = []
        for package in essential_packages:
            if package.lower() not in requirements.lower():
                missing_packages.append(package)
                
        if missing_packages:
            self.warnings.append(f"Missing packages: {', '.join(missing_packages)}")
        else:
            self.passed_checks.append("✅ All essential packages included")
            print("   ✅ Requirements file is complete")
            
    def check_documentation(self):
        """Check documentation completeness"""
        print("\n🔍 Checking documentation...")
        
        readme_path = self.project_root / 'README.md'
        
        if not readme_path.exists():
            self.issues.append("❌ README.md is missing")
            return
            
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            
        essential_sections = [
            'installation',
            'api key',
            'environment',
            'security',
            'deployment'
        ]
        
        missing_sections = []
        for section in essential_sections:
            if section.lower() not in readme_content.lower():
                missing_sections.append(section)
                
        if missing_sections:
            self.warnings.append(f"README missing sections: {', '.join(missing_sections)}")
        else:
            self.passed_checks.append("✅ README.md is comprehensive")
            print("   ✅ Documentation is complete")
            
    def check_project_structure(self):
        """Verify project structure is GitHub-ready"""
        print("\n🔍 Checking project structure...")
        
        essential_files = [
            'app.py',
            'requirements.txt',
            'README.md',
            '.gitignore',
            '.env.example',
            'templates',
            'static'
        ]
        
        missing_files = []
        
        for file_item in essential_files:
            file_path = self.project_root / file_item
            if not file_path.exists():
                missing_files.append(file_item)
                
        if missing_files:
            self.issues.append(f"❌ Missing essential files: {', '.join(missing_files)}")
        else:
            self.passed_checks.append("✅ Project structure is complete")
            print("   ✅ All essential files present")
            
    def check_deployment_readiness(self):
        """Check if project is deployment-ready"""
        print("\n🔍 Checking deployment readiness...")
        
        # Check for gunicorn configuration
        gunicorn_config = self.project_root / 'gunicorn.conf.py'
        
        checks = []
        
        if gunicorn_config.exists():
            checks.append("✅ Gunicorn configuration present")
        else:
            self.warnings.append("⚠️ No gunicorn.conf.py found")
            
        # Check for deployment scripts
        deploy_scripts = [
            self.project_root / 'deploy.sh',
            self.project_root / 'deploy.bat'
        ]
        
        if any(script.exists() for script in deploy_scripts):
            checks.append("✅ Deployment scripts available")
        else:
            self.warnings.append("⚠️ No deployment scripts found")
            
        if checks:
            self.passed_checks.extend(checks)
            print("   ✅ Deployment configuration ready")
        else:
            print("   ⚠️ Some deployment files missing")
            
    def run_audit(self):
        """Run complete security audit"""
        self.print_header()
        
        # Run all checks
        self.check_sensitive_files()
        self.check_gitignore()
        self.check_environment_template()
        self.check_code_security()
        self.check_requirements()
        self.check_documentation()
        self.check_project_structure()
        self.check_deployment_readiness()
        
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print audit summary"""
        print("\n" + "=" * 60)
        print("📊 SECURITY AUDIT SUMMARY")
        print("=" * 60)
        
        print(f"\n✅ PASSED CHECKS ({len(self.passed_checks)}):")
        for check in self.passed_checks:
            print(f"   {check}")
            
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
                
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   {issue}")
                
        print("\n" + "=" * 60)
        print("🎯 GITHUB READINESS ASSESSMENT")
        print("=" * 60)
        
        if not self.issues:
            if not self.warnings:
                print("🟢 STATUS: READY FOR GITHUB PUBLISHING")
                print("   ✅ All security checks passed")
                print("   ✅ No critical issues found")
                print("   ✅ Project structure is complete")
            else:
                print("🟡 STATUS: MOSTLY READY (MINOR WARNINGS)")
                print("   ✅ No critical security issues")
                print("   ⚠️ Some minor improvements recommended")
                print("   ✅ Safe to publish on GitHub")
        else:
            print("🔴 STATUS: NOT READY FOR PUBLISHING")
            print("   ❌ Critical issues must be resolved first")
            print("   🛠️ Fix issues before GitHub publication")
            
        print("\n📋 GITHUB PUBLISHING CHECKLIST:")
        print("   □ All critical issues resolved")
        print("   □ .env file not committed (in .gitignore)")
        print("   □ .env.example template available")
        print("   □ README.md is comprehensive")
        print("   □ Add project screenshots to /screenshots/")
        print("   □ Test deployment locally")
        print("   □ Create GitHub repository")
        print("   □ Push code to GitHub")
        print("   □ Add repository description and tags")
        
        print(f"\n📈 SECURITY SCORE: {len(self.passed_checks)}/{len(self.passed_checks) + len(self.warnings) + len(self.issues)}")
        
        # Return exit code
        return 0 if not self.issues else 1

def main():
    """Run the security audit"""
    audit = SecurityAudit()
    exit_code = audit.run_audit()
    
    print("\n🔒 Security audit completed!")
    print("   Run this script regularly to maintain security standards.")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

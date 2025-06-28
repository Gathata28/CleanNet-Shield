# Contributing to CleanNet Shield

Thank you for your interest in contributing to CleanNet Shield! This project aims to support individuals in their recovery journey by providing effective content blocking and recovery tools.

## 🤝 How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or request features
- Provide clear, detailed descriptions
- Include system information (Windows version, Python version)
- Attach relevant log files from `data/logs/`

### Suggesting Features

- Check existing issues first to avoid duplicates
- Explain the use case and benefit
- Consider privacy and security implications
- Focus on features that support recovery goals

### Code Contributions

#### Before You Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Read through the existing code to understand the architecture

#### Coding Standards

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Include comprehensive docstrings
- Add error handling and logging
- Maintain the modular architecture

#### Testing

- Add tests for new functionality
- Ensure all existing tests pass
- Test on Windows 10/11 environments
- Verify admin privilege requirements work correctly

#### Documentation

- Update relevant documentation in `docs/`
- Add comments for complex logic
- Update the README if needed
- Include usage examples

### Areas We Need Help With

#### High Priority

- **Security Enhancements**: Tamper protection, watchdog services
- **File System Monitoring**: Detect suspicious files in downloads
- **Browser Integration**: Advanced browser-level blocking
- **Performance Optimization**: Reduce resource usage

#### Medium Priority

- **Additional Blocklist Sources**: More comprehensive coverage
- **UI/UX Improvements**: Better user experience
- **Recovery Features**: Enhanced analytics and insights
- **Cross-Platform Support**: Linux and macOS compatibility

#### Low Priority

- **Cloud Integration**: Optional cloud sync features
- **Mobile Companion**: Android/iOS app integration
- **Advanced Analytics**: Machine learning insights

## 📋 Development Setup

1. **Clone your fork**:

   ```bash
   git clone https://github.com/yourusername/cleannet-shield.git
   cd cleannet-shield
   ```

2. **Set up development environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Run tests**:

   ```bash
   python scripts\test_suite.py
   ```

4. **Test the application**:

   ```bash
   python launcher.py
   ```

## 🔐 Security Considerations

### Privacy First

- Never log or transmit personal data
- Keep all recovery data local by default
- Implement proper data encryption for sensitive information
- Respect user privacy in all features

### Security Guidelines

- Validate all external inputs
- Use secure methods for system modifications
- Implement proper privilege escalation
- Avoid creating security vulnerabilities

### Responsible Development

- Consider the impact on users' recovery journey
- Test thoroughly to avoid breaking protection features
- Document any security implications
- Follow ethical development practices

## 📝 Pull Request Process

1. **Prepare your changes**:
   - Ensure code follows style guidelines
   - Add/update tests and documentation
   - Test thoroughly on Windows

2. **Create a clear PR description**:
   - Explain what changes were made and why
   - Reference any related issues
   - Include testing details
   - Note any breaking changes

3. **Review process**:
   - Maintainers will review your code
   - Address any feedback promptly
   - Be patient - thorough review takes time
   - Be open to suggestions and improvements

## 🎯 Project Values

### Recovery-Focused

- Every feature should support the recovery journey
- Avoid creating features that could be misused
- Consider the psychological impact of changes
- Prioritize user well-being over technical sophistication

### Privacy & Security

- User data stays on their device
- No tracking or analytics without explicit consent
- Secure by default
- Transparent about what the software does

### Accessibility

- Easy to install and use
- Clear documentation
- Support for non-technical users
- Helpful error messages

### Quality

- Robust error handling
- Comprehensive testing
- Clean, maintainable code
- Professional documentation

## 🚨 Code of Conduct

### Be Respectful

- Treat all contributors with respect
- Focus on constructive feedback
- Avoid judgment about personal struggles
- Maintain a supportive environment

### Be Professional

- Keep discussions technical and solution-focused
- Avoid personal attacks or discrimination
- Respect different perspectives and experiences
- Maintain confidentiality about sensitive topics

### Be Helpful

- Welcome new contributors
- Share knowledge and experience
- Provide clear feedback
- Support the community goals

## 📞 Getting Help

- **Technical Questions**: Open a GitHub issue
- **Development Setup**: Check the documentation
- **General Discussion**: Use GitHub Discussions
- **Security Issues**: Email maintainers directly

## 🎉 Recognition

Contributors will be:

- Listed in the project contributors
- Acknowledged in release notes
- Invited to provide input on project direction
- Welcomed as part of the recovery support community

---

Thank you for helping make CleanNet Shield better for everyone on their recovery journey! 🛡️💪

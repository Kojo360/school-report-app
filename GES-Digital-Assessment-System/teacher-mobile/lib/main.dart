import 'package:flutter/material.dart';

import 'data/local_database.dart';

void main() => runApp(const TeacherMobileApp());

class TeacherMobileApp extends StatelessWidget {
  const TeacherMobileApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'GES Teacher',
        theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
        home: const LoginScreen(),
      );
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _username = TextEditingController();
  final _password = TextEditingController();

  @override
  void dispose() {
    _username.dispose();
    _password.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 400),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                const Text('GES Teacher', style: TextStyle(fontSize: 28)),
                const SizedBox(height: 24),
                TextField(controller: _username, decoration: const InputDecoration(labelText: 'Username')),
                TextField(controller: _password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
                const SizedBox(height: 20),
                FilledButton(
                  onPressed: () {
                    if (_username.text.trim().isEmpty || _password.text.isEmpty) return;
                    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const TeacherHome()));
                  },
                  child: const Text('Log in'),
                ),
              ]),
            ),
          ),
        ),
      );
}

class TeacherHome extends StatefulWidget {
  const TeacherHome({super.key});

  @override
  State<TeacherHome> createState() => _TeacherHomeState();
}

class _TeacherHomeState extends State<TeacherHome> {
  int _tab = 0;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('GES Teacher')),
        body: _tab == 0 ? const StudentList() : const GradeEntry(),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _tab,
          onDestinationSelected: (value) => setState(() => _tab = value),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.people), label: 'Students'),
            NavigationDestination(icon: Icon(Icons.edit_note), label: 'Enter grade'),
          ],
        ),
      );
}

class StudentList extends StatefulWidget {
  const StudentList({super.key});

  @override
  State<StudentList> createState() => _StudentListState();
}

class _StudentListState extends State<StudentList> {
  late Future<List<Map<String, Object?>>> _students;

  @override
  void initState() {
    super.initState();
    _students = LocalDatabase.instance.getStudents();
  }

  void _reload() => setState(() => _students = LocalDatabase.instance.getStudents());

  @override
  Widget build(BuildContext context) => Scaffold(
        floatingActionButton: FloatingActionButton(
          onPressed: () async {
            final added = await showDialog<bool>(context: context, builder: (_) => const AddStudentDialog());
            if (added == true) _reload();
          },
          child: const Icon(Icons.person_add),
        ),
        body: FutureBuilder<List<Map<String, Object?>>>(
          future: _students,
          builder: (context, snapshot) {
            final students = snapshot.data ?? [];
            if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
            if (students.isEmpty) return const Center(child: Text('No local students yet.'));
            return ListView.builder(
              itemCount: students.length,
              itemBuilder: (_, index) => ListTile(
                title: Text(students[index]['full_name']! as String),
                subtitle: const Text('Pending sync'),
              ),
            );
          },
        ),
      );
}

class AddStudentDialog extends StatefulWidget {
  const AddStudentDialog({super.key});
  @override
  State<AddStudentDialog> createState() => _AddStudentDialogState();
}

class _AddStudentDialogState extends State<AddStudentDialog> {
  final _name = TextEditingController();
  final _dob = TextEditingController();
  final _admissionDate = TextEditingController();

  @override
  Widget build(BuildContext context) => AlertDialog(
        title: const Text('Add student'),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          TextField(controller: _name, decoration: const InputDecoration(labelText: 'Full name')),
          TextField(controller: _dob, decoration: const InputDecoration(labelText: 'Date of birth (YYYY-MM-DD)')),
          TextField(controller: _admissionDate, decoration: const InputDecoration(labelText: 'Admission date (YYYY-MM-DD)')),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(
            onPressed: () async {
              await LocalDatabase.instance.addStudent(fullName: _name.text, dob: _dob.text, admissionDate: _admissionDate.text);
              if (context.mounted) Navigator.pop(context, true);
            },
            child: const Text('Save offline'),
          ),
        ],
      );
}

class GradeEntry extends StatefulWidget {
  const GradeEntry({super.key});
  @override
  State<GradeEntry> createState() => _GradeEntryState();
}

class _GradeEntryState extends State<GradeEntry> {
  int? _studentId;
  final _subject = TextEditingController();
  final _score = TextEditingController();

  @override
  Widget build(BuildContext context) => FutureBuilder<List<Map<String, Object?>>>(
        future: LocalDatabase.instance.getStudents(),
        builder: (context, snapshot) {
          final students = snapshot.data ?? [];
          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(children: [
              DropdownButtonFormField<int>(
                initialValue: _studentId,
                decoration: const InputDecoration(labelText: 'Student'),
                items: students.map((student) => DropdownMenuItem(value: student['id']! as int, child: Text(student['full_name']! as String))).toList(),
                onChanged: (value) => setState(() => _studentId = value),
              ),
              TextField(controller: _subject, decoration: const InputDecoration(labelText: 'Subject')),
              TextField(controller: _score, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Score')),
              const SizedBox(height: 20),
              FilledButton(
                onPressed: () async {
                  final score = double.tryParse(_score.text);
                  if (_studentId == null || _subject.text.isEmpty || score == null) return;
                  await LocalDatabase.instance.addGrade(studentId: _studentId!, subject: _subject.text, score: score);
                  if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Grade saved locally (PENDING sync).')));
                },
                child: const Text('Save grade offline'),
              ),
            ]),
          );
        },
      );
}

# GES Teacher Mobile

Offline-first Flutter application for teachers. SQLite stores `local_students`, `local_grades`, and `sync_queue`; records are queued with `PENDING` status for a future backend synchronization service.

After a working Flutter SDK is available, run:

```powershell
flutter create . --project-name teacher_mobile --platforms android
flutter pub get
flutter run
```

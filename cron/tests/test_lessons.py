import datetime
import logging
from django.utils import timezone
from cjwstate.models import Workflow
from cjwstate.tests.utils import DbTestCase
from cron import lessons


StaleTimedelta = datetime.timedelta(days=7.1)
FreshTimedelta = datetime.timedelta(days=1.1)


class DisableStaleAutoUpdateTests(DbTestCase):
    def test_disable_auto_update_on_stale_lesson(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - StaleTimedelta),
            lesson_slug="analyze-live-twitter",
        )
        tab = workflow.tabs.first()
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=True,
            next_update=timezone.now(),
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, False)
        self.assertIsNone(wf_module.next_update)

    def test_ignore_non_auto_update_wfmodule(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - StaleTimedelta),
            lesson_slug="analyze-live-twitter",
        )
        tab = workflow.tabs.first()
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=False,
            next_update=None,
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, False)
        self.assertIsNone(wf_module.next_update)

    def test_ignore_deleted_wfmodule(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - StaleTimedelta),
            lesson_slug="analyze-live-twitter",
        )
        tab = workflow.tabs.first()
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=True,
            next_update=timezone.now(),
            is_deleted=True,
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, True)
        self.assertIsNotNone(wf_module.next_update)

    def test_ignore_deleted_tab(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - StaleTimedelta),
            lesson_slug="analyze-live-twitter",
        )
        tab = workflow.tabs.create(position=1, slug="tab-deleted", is_deleted=True)
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=True,
            next_update=timezone.now(),
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, True)
        self.assertIsNotNone(wf_module.next_update)

    def test_ignore_fresh_lesson(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - FreshTimedelta),
            lesson_slug="analyze-live-twitter",
        )
        tab = workflow.tabs.first()
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=True,
            next_update=timezone.now(),
            is_deleted=True,
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, True)
        self.assertIsNotNone(wf_module.next_update)

    def test_ignore_stale_non_lesson(self):
        workflow = Workflow.create_and_init(
            last_viewed_at=(timezone.now() - StaleTimedelta), lesson_slug=None
        )
        tab = workflow.tabs.first()
        wf_module = tab.wf_modules.create(
            order=0,
            slug="step-1",
            module_id_name="fetcher",
            auto_update_data=True,
            next_update=timezone.now(),
            is_deleted=True,
        )
        with self.assertLogs(lessons.__name__, logging.INFO):
            self.run_with_async_db(lessons.disable_stale_auto_update())
        wf_module.refresh_from_db()
        self.assertEqual(wf_module.auto_update_data, True)
        self.assertIsNotNone(wf_module.next_update)

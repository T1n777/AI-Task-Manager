import wx
from database import create_table
from task_manager import add_task, get_tasks, mark_done, delete_task
from perplexity_ai import ask_ai


class TaskApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="AI Task Manager", size=(700, 500))
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        
        self.title_input = wx.TextCtrl(panel)
        self.title_input.SetHint("Title")

        self.desc_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 60))
        self.desc_input.SetHint("Task description")

        self.deadline_input = wx.TextCtrl(panel)
        self.deadline_input.SetHint("Deadline (DD-MM-YYYY)")

        main_sizer.Add(self.title_input, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.desc_input, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.deadline_input, 0, wx.EXPAND | wx.ALL, 5)

        
        add_btn = wx.Button(panel, label="Add Task (AI decides priority)")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_task)
        main_sizer.Add(add_btn, 0, wx.ALL, 5)

        
        self.task_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.task_list.InsertColumn(0, "ID", width=50)
        self.task_list.InsertColumn(1, "Title", width=250)
        self.task_list.InsertColumn(2, "Priority", width=80)
        self.task_list.InsertColumn(3, "Status", width=100)

        main_sizer.Add(self.task_list, 1, wx.EXPAND | wx.ALL, 5)

        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        done_btn = wx.Button(panel, label="Mark Done")
        delete_btn = wx.Button(panel, label="Delete")

        done_btn.Bind(wx.EVT_BUTTON, self.on_mark_done)
        delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)

        btn_sizer.Add(done_btn, 0, wx.ALL, 5)
        btn_sizer.Add(delete_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer)

        
        self.ai_input = wx.TextCtrl(panel)
        self.ai_input.SetHint("Ask AI about your tasks...")

        ai_btn = wx.Button(panel, label="Ask AI")
        ai_btn.Bind(wx.EVT_BUTTON, self.on_ask_ai)

        main_sizer.Add(self.ai_input, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(ai_btn, 0, wx.ALL, 5)

        panel.SetSizer(main_sizer)

        self.refresh_tasks()

    
    def refresh_tasks(self):
        self.task_list.DeleteAllItems()
        for task in get_tasks():
            index = self.task_list.InsertItem(
                self.task_list.GetItemCount(), str(task[0])
            )
            self.task_list.SetItem(index, 1, task[1])
            self.task_list.SetItem(index, 2, str(task[4]))
            self.task_list.SetItem(index, 3, task[5])

    
    def on_add_task(self, event):
        title = self.title_input.GetValue().strip()
        desc = self.desc_input.GetValue().strip()
        deadline = self.deadline_input.GetValue().strip()

        if not title:
            wx.MessageBox(
                "Title cannot be empty.",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return

        prompt = f"""
Assign a priority from 1 (low) to 5 (high).

Task title: {title}
Description: {desc}
Deadline: {deadline}

Respond with ONLY a number between 1 and 5.
"""

        try:
            raw_response = ask_ai(prompt)
            print("AI raw response:", raw_response)

            priority = None
            for ch in raw_response:
                if ch in "12345":
                    priority = int(ch)
                    break

            if priority is None:
                priority = 3  

        except Exception as e:
            print("AI error:", e)
            priority = 3  

        add_task(title, desc, deadline, priority)
        self.refresh_tasks()

        self.title_input.Clear()
        self.desc_input.Clear()
        self.deadline_input.Clear()

    def on_mark_done(self, event):
        selected = self.task_list.GetFirstSelected()
        if selected == -1:
            return

        task_id = int(self.task_list.GetItemText(selected))
        mark_done(task_id)
        self.refresh_tasks()

    def on_delete(self, event):
        selected = self.task_list.GetFirstSelected()
        if selected == -1:
            return

        task_id = int(self.task_list.GetItemText(selected))
        delete_task(task_id)
        self.refresh_tasks()

    def on_ask_ai(self, event):
        question = self.ai_input.GetValue().strip()
        if not question:
            return

        tasks = get_tasks()

        if not tasks:
            wx.MessageBox(
                "You have no tasks stored.",
                "AI Response",
                wx.OK | wx.ICON_INFORMATION
            )
            return

        task_lines = []
        for t in tasks:
            task_lines.append(
                f"ID {t[0]}: {t[1]} (priority {t[4]}, status {t[5]})"
            )

        task_block = "\n".join(task_lines)

        prompt = f"""
You are given the user's ACTUAL task list below.
This list is complete and authoritative.
DO NOT use external knowledge.
DO NOT assume missing tasks.

TASK LIST:
{task_block}

USER QUESTION:
{question}

Answer ONLY using the task list above.
"""

        try:
            response = ask_ai(prompt)
            wx.MessageBox(
                response,
                "AI Response",
                wx.OK | wx.ICON_INFORMATION
            )
        except Exception as e:
            print("AI error:", e)
            wx.MessageBox(
                "AI request failed.",
                "Error",
                wx.OK | wx.ICON_ERROR
        )



if __name__ == "__main__":
    create_table()
    app = wx.App(False)
    frame = TaskApp()
    frame.Show()
    app.MainLoop()



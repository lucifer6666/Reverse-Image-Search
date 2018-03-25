from tkinter import *
from PyQt4 import QtGui,QtCore
import cv2
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window,self).__init__(parent)
        self.setGeometry(150,150,680,565)
        self.setWindowTitle('Motion Scanner')
        self.video = QtGui.QLabel('', self)
        self.video.setGeometry(20, 20, 640, 485)
        self.btn1 = QtGui.QPushButton('Start', self)
        self.btn1.setGeometry(50, 515, 100, 30)
        self.btn1.clicked.connect(self.Start)
        self.btn3 = QtGui.QPushButton('Scan', self)
        self.btn3.setGeometry(170, 515, 100, 30)
        self.btn3.clicked.connect(self.Stop)
        self.output = QtGui.QLabel('', self)
        self.output.setGeometry(290, 515, 150, 30)
        myPixmap = QtGui.QPixmap("I:/projects/py/loadin/camera.jpg")
        myScaledPixmap = myPixmap.scaled(self.video.size())
        self.video.setPixmap(myScaledPixmap)
        self.cap = cv2.VideoCapture(1)
        self.show()
    def Start(self):
        self.fps=30
        self.timer = QtCore.QTimer()
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.a=frame
        self.video.setPixmap(pix)
        self.timer.timeout.connect(self.Start)
        self.timer.start(1000. / self.fps)

    def Stop(self):
        cv2.imwrite("Scan1.jpg", self.a)
        self.timer.stop()
        opts = Options()
        opts.set_headless()
        assert opts.headless
        driver = Firefox(options=opts)
        # navigate to the application home page
        driver.get("https://images.google.com/")
        # click on camera image
        search_field = driver.find_element_by_id("qbi")
        search_field.click()
        driver.find_element_by_class_name('qbtbha.qbtbtxt.qbclr').click()
        # clicking on upload image
        b = driver.find_element_by_css_selector("input[type=\"file\"]")
        b.clear()
        # uploading image
        b.send_keys("I:\\\\projects\\\\py\\\\Scan1.jpg")
        search_form = driver.find_element_by_id('mKlEF')
        search_form.submit()
        driver.implicitly_wait(30)
        # getting results
        RESULTS_LOCATOR = "//div/h3/a"
        # WebDriverWait(driver, 10).until(
        #    EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
        page1_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)
        a = " "
        # storing all the results in a
        for item in page1_results:
            a += item.text
        print()
        # finding the most repeated word and showing it
        frequency = {}
        document_text = a
        text_string = document_text.lower()
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
        for word in match_pattern:
            count = frequency.get(word, 0)
            frequency[word] = count + 1
        # frequency_list = frequency.keys()
        result=max(frequency.keys(), key=(lambda k: frequency[k]))
        print(max(frequency.keys(), key=(lambda k: frequency[k])))
        cv2.putText(self.a, result, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 3, 4)
        self.output.setText(result)
        driver.close()

app=QtGui.QApplication(sys.argv)
GUI=Window()
sys.exit(app.exec_())
<script setup>
import { ref } from "vue";
import { lyla } from "lyla";
import { useMessage } from "naive-ui";
const message = useMessage();
const DataFromServer = ref([]);
const sampleName = ref(4);
const barcode = ref(23);
const chip = ref(27);
const lane = ref(28);
const datapath = ref(48);
const path = ref("10.2.100.1:/pakpox/pob8d1/");
const code1 = ref("");
const code2 = ref("");
const tableUpload = ref();
const params = ref({
  sampleName: sampleName,
  barcode: barcode,
  chip: chip,
  lane: lane,
  datapath: datapath,
  path: path,
});
const params2 = ref({
  file: "",
  sampleName: sampleName,
  barcode: barcode,
  chip: chip,
  lane: lane,
  datapath: datapath,
  path: path,
});
const customUpload = ({
  file,
  data,
  headers,
  withCredentials,
  action,
  onFinish,
  onError,
  onProgress,
}) => {
  const formData = new FormData();
  params2.value.file = file.file;
  if (data) {
    Object.keys(data).forEach((key) => {
      formData.append(key, data[key]);
    });
  }
  formData.append("file", file.file);
  lyla
    .post(action, {
      withCredentials,
      headers,
      body: formData,
      onUploadProgress: ({ percent }) => {
        onProgress({ percent: Math.ceil(percent) });
      },
    })
    .then(({ json }) => {
      if (json.hasBlank == 1) {
        message.warning("Upload success, but some blank in table");
      }
      if (json.hasDup == 1) {
        message.warning("Upload success, but some duplicate in table");
      }
      DataFromServer.value = json.rawData;
      code1.value = json.cmd1;
      code2.value = json.cmd2;
      onFinish();
    })
    .catch((error) => {
      message.success(error.message);
      onError();
    });
};
const customUpload2 = ({
  file,
  data,
  headers,
  withCredentials,
  action,
  onFinish,
  onError,
  onProgress,
}) => {
  const formData = new FormData();
  params2.value.file2 = file.file;
  if (data) {
    Object.keys(data).forEach((key) => {
      formData.append(key, data[key]);
    });
  }
  formData.append("file2", file.file);
  lyla
    .post(action, {
      withCredentials,
      headers,
      body: formData,
      onUploadProgress: ({ percent }) => {
        onProgress({ percent: Math.ceil(percent) });
      },
    })
    .then(({ json }) => {
      if (json.hasBlank == 1) {
        message.warning("Upload success, but some blank in table");
      }
      if (json.hasDup == 1) {
        message.warning("Upload success, but some duplicate in table");
      }
      DataFromServer.value = json.rawData;
      code1.value = json.cmd1;
      code2.value = json.cmd2;
      onFinish();
    })
    .catch((error) => {
      message.success(error.message);
      onError();
    });
};
const columns = [
  {
    title: "sampleName",
    key: "sampleName",
  },
  {
    title: "barcode",
    key: "barcode",
  },
  {
    title: "chip",
    key: "chip",
  },
  {
    title: "lane",
    key: "lane",
  },
  {
    title: "dataPath",
    key: "dataPath",
    width: 100,
    ellipsis: {
      tooltip: true,
    },
  },
];
const submitdata = () => {
  tableUpload.value?.submit();
};
</script>
<template>
  <n-layout>
    <n-layout-header bordered>
      <div style="margin: 10px 12px;">
      <span style="font-size: 1.3rem;font-weight: 500;">Glims to copy</span>
    </div>
    </n-layout-header>
    <n-layout-content>
      <div style="margin-top: 20px;">
      <n-grid x-gap="12" :cols="12">
        <n-gi :span="1"> </n-gi>
        <n-gi :span="3">
          <n-card hoverable>
            <n-space vertical>
              <n-p>Excel from Glims...</n-p>
              <n-upload
                ref="tableUpload"
                :default-upload="false"
                action="https://glims2excel-1-w4936186.deta.app/upload"
                response-type="json"
                :custom-request="customUpload"
                :data="params"
              >
                <n-button style="height: 35px">Upload..</n-button>
              </n-upload>

              <n-p>Index for sampleName</n-p>
              <n-input-number v-model:value="sampleName" clearable />
              <n-p>Index for barcode</n-p>
              <n-input-number v-model:value="barcode" clearable />
              <n-p>Index for chip</n-p>
              <n-input-number v-model:value="chip" clearable />
              <n-p>Index for lane</n-p>
              <n-input-number v-model:value="lane" clearable />
              <n-p>Index for dataPath</n-p>
              <n-input-number v-model:value="datapath" clearable />
              <n-p>Remoth path</n-p>
              <n-input v-model:value="path" type="text" />
              <n-button type="error" @click="submitdata"> Submit! </n-button>
              <n-divider dashed> Change Names </n-divider>
              <n-upload
                action="https://glims2excel-1-w4936186.deta.app/changenames"
                response-type="json"
                :custom-request="customUpload2"
                :data="params2"
              >
                <n-button round type="primary">Upload..</n-button>
              </n-upload>
            </n-space>
          </n-card>
        </n-gi>
        <n-gi :span="7">
          <n-space vertical style="margin-top: 50px">
            <n-tabs type="segment">
              <n-tab-pane name="table" tab="Table Preview">
                <n-data-table
                  :columns="columns"
                  :data="DataFromServer"
                  max-height="600px"
                />
              </n-tab-pane>
              <n-tab-pane name="cmd" tab="Shell cmd">
                <n-tabs type="line" animated>
                  <n-tab-pane name="shell1" tab="Shell1">
                    <n-card style="overflow-y: scroll; max-height: 700px">
                      <n-code :code="code1" language="bash" word-wrap> </n-code>
                    </n-card>
                  </n-tab-pane>
                  <n-tab-pane name="shell2" tab="Shell2">
                    <n-card style="overflow-y: scroll; max-height: 700px">
                      <n-code :code="code2" language="bash" word-wrap> </n-code>
                    </n-card>
                  </n-tab-pane>
                </n-tabs>
              </n-tab-pane>
            </n-tabs>
          </n-space>
        </n-gi>
        <n-gi :span="1"> </n-gi>
      </n-grid>
      </div>
    </n-layout-content>
    <n-layout-footer> 
      <div style="height: 90px;text-align: center;padding-top: 30px;">
        <p>built by XiaoguangPan</p>
        <p>Based on Vue.js & Naive UI</p>
      </div>
       </n-layout-footer>
  </n-layout>
</template>

<style scoped></style>

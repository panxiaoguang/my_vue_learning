<script setup>
import { ref } from "vue";
import axios from "axios";
import { useMessage } from "naive-ui";

const message = useMessage();
const DataFromServer = ref([]);
const changes = ref([]);
function checkForEmpty(obj) {
  return Object.values(obj).some(value => value === null || value === undefined || value === '');
}

const handleFinish = ({ file, event }) => {
  DataFromServer.value = (event?.target).response;
  message.success("Upload success");
  if (DataFromServer.value.some(obj => checkForEmpty(obj))) {
    message.error("blank value detected, please check your excel file!");
  }
  return file;
};
const code1 = ref();
const code2 = ref();
const model = ref({
  sampleName: "4",
  barcode: "23",
  chip: "27",
  lane: "28",
  datapath: "48",
  path: "10.2.100.1:/pakpox/pob8d1/",
  content: null,
});
const columns = [
  {
    title: "sampleName",
    key: "n" + model.value.sampleName,
  },
  {
    title: "Barcode",
    key: "n" + model.value.barcode,
  },
  {
    title: "Chip",
    key: "n" + model.value.chip,
  },
  {
    title: "Lane",
    key: "n" + model.value.lane,
  },
  {
    title: "DataPath",
    key: "n" + model.value.datapath,
  },
];

const submitdata = () => {
  model.value.content = DataFromServer.value.map((obj) => ({
    ["n1"]: obj[columns[0].key],
    ["n2"]: obj[columns[1].key],
    ["n3"]: obj[columns[2].key],
    ["n4"]: obj[columns[3].key],
    ["n5"]: obj[columns[4].key],
  }));
  axios
    .post("http://127.0.0.1:8000/test", model.value)
    .then(function (response) {
      code1.value = response.data.cmd1;
      code2.value = response.data.cmd2;
    })
    .catch(function (error) {
      console.log(error);
    });
};
const replaceName = ({ file, event }) => {
  changes.value = (event?.target).response;
  return file;
};
const changeNames = () => {
  axios
    .post("http://127.0.0.1:8000/change", {
      path: model.value.path,
      content: model.value.content,
      changes: changes.value,
    })
    .then(function (response) {
      code1.value = response.data.cmd1;
      code2.value = response.data.cmd2;
    })
    .catch(function (error) {
      console.log(error);
    });
}
</script>
<template>
  <n-grid x-gap="12" :cols="12">
    <n-gi :span="1"> </n-gi>
    <n-gi :span="3">
      <n-space vertical style="margin-top: 50px">
        <n-space style="align-items: center">
          <n-upload
            action="http://127.0.0.1:8000/upload"
            response-type="json"
            @finish="handleFinish"
          >
            <n-button round type="primary">Upload..</n-button>
          </n-upload>
          <n-text>Excel file from Glims...</n-text>
        </n-space>
        <n-form :model="model">
          <n-form-item path="samplename" label="Index for sampleName">
            <n-input v-model:value="model.sampleName" @keydown.enter.prevent />
          </n-form-item>
          <n-form-item path="barcode" label="Index for barcode">
            <n-input v-model:value="model.barcode" @keydown.enter.prevent />
          </n-form-item>
          <n-form-item path="chip" label="Index for chip">
            <n-input v-model:value="model.chip" @keydown.enter.prevent />
          </n-form-item>
          <n-form-item path="lane" label="Index for lane">
            <n-input v-model:value="model.lane" @keydown.enter.prevent />
          </n-form-item>
          <n-form-item path="datapath" label="Index for dataPath">
            <n-input v-model:value="model.datapath" @keydown.enter.prevent />
          </n-form-item>
          <n-form-item path="path" label="Remoth path">
            <n-input v-model:value="model.path" @keydown.enter.prevent />
          </n-form-item>
          <n-button type="error" @click="submitdata">
            Submit!
          </n-button>
        </n-form>
        <n-divider dashed> Next-Step </n-divider>
        <n-space justify="space-between">
          <n-upload
            action="http://127.0.0.1:8000/receivename"
            response-type="json"
            @finish="replaceName"
          >
            <n-button round type="primary">Upload..</n-button>
          </n-upload>
          <n-button type="error" @click="changeNames">
            ChangeNames!
          </n-button>
        </n-space>
      </n-space>
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
                <n-card>
                <n-code :code="code1" language="bash" word-wrap> </n-code>
              </n-card>
              </n-tab-pane>
              <n-tab-pane name="shell2" tab="Shell2">
                <n-card>
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
</template>

<style scoped></style>

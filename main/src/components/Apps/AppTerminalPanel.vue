<!--
  * @LastEditors: zhanghengxin ezreal.zhang@icewhale.org
  * @LastEditTime: 2023/3/2 下午4:26
  * @FilePath: /CasaOS-UI/src/components/Apps/AppTerminalPanel.vue
  * @Description:
  *
  * Copyright (c) 2023 by IceWhale, All Rights Reserved.
  
  -->

<template>
	<div class="modal-card">

		<!-- Modal-Card Body Start -->
		<section class="modal-card-body ">
			<div class="close-container">
				<button class="delete" type="button" @click="$emit('close')"/>
			</div>
			<h3 class="title is-3">{{ serviceName || appName }}</h3>
			<div class="is-flex-grow-1">
				<b-tabs :animated="false" @input="onInput">
					<b-tab-item :label="$t('Terminal')" value="terminal">
						<terminal-card ref="terminal" :initWsUrl="wsUrl"></terminal-card>
					</b-tab-item>
					<b-tab-item :label="$t('Logs')" value="logs">
						<logs-card ref="logs" :data="logData"></logs-card>
					</b-tab-item>
				</b-tabs>

			</div>

		</section>
		<!-- Modal-Card Body End -->

		<b-loading v-model="isLoading" :is-full-page="false"></b-loading>
	</div>
</template>

<script>
import TerminalCard from '@/components/logsAndTerminal/TerminalCard.vue';
import LogsCard     from '@/components/logsAndTerminal/LogsCard.vue'

export default {
	name: 'app-terminal-panel',
	components: {
		TerminalCard,
		LogsCard
	},
	data() {
		return {
			isLoading: false,
			wsUrl: `${this.$wsProtocol}//${this.$baseURL}/v1/container/${this.appid}/terminal?token=${this.$store.state.access_token}`,
			logData: "",
			timer: "",
		}
	},
	props: {
		appid: String,
		appName: String,
		serviceName: String,
	},
	mounted() {
		this.getLogs();
		this.timer = setInterval(() => {
			this.getLogs();
		}, 1000 * 5);
	},
	methods: {
		getLogs() {
			// OLD:: this.$api.container.getLogsV2(this.appid)
			this.$openAPI.appManagement.compose.composeAppLogs(this.appName).then((res) => {
				if (res.status == 200) {
					// let data = res.data.data
					// console.log(data)
					// let replaceData = data.replace(/\n(.{8})/gu, '\n');
					// this.logData = replaceData.substring(8, replaceData.length - 1);
					this.logData = res.data.data
				}
			}).catch((err) => {
				console.log('$openAPI.appManagement.compose.composeAppLogs', err)
			})
		},
		onInput(e) {
			if (e == "terminal") {
				this.$refs.terminal.active(true)
				this.$refs.logs.active(false)
			} else {
				this.$refs.terminal.active(false)
				this.$refs.logs.active(true)
			}
		}
	},
	destroyed() {
		clearInterval(this.timer);
	}
}
</script>

<style>
</style>

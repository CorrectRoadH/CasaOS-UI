<!--
 * @Author: Jerryk jerry@icewhale.org
 * @Date: 2022-02-18 10:20:10
 * @LastEditors: Jerryk jerry@icewhale.org
 * @LastEditTime: 2022-07-15 17:58:36
 * @FilePath: /CasaOS-UI/src/components/logsAndTerminal/TerminalPanel.vue
 * @Description:
 *
 * Copyright (c) 2022 by IceWhale, All Rights Reserved.
-->
<template>
	<div class="modal-card">

		<!-- Modal-Card Body Start -->
		<section class="modal-card-body " style="overflow:hidden">
			<h3 class="title is-3">CasaOS</h3>
			<div class="close-container">
				<span v-show="showTabName === 'logs'" class="mdi mdi-tray-arrow-down is-size-20px mr-4 cursor-pointer"
					  @click="downloadSystemLog"></span>
				<button class="delete" type="button" @click="$emit('close')"/>
			</div>
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
import TerminalCard from './TerminalCard.vue';
import LogsCard     from './LogsCard.vue';
import qs           from "qs";

export default {
	name: 'terminal-panel',
	components: {
		TerminalCard,
		LogsCard
	},
	data() {
		return {
			isLoading: false,
			wsUrl: ``,
			logData: "",
			timer: '',
			showTabName: "terminal"
		}
	},
	mounted() {
		this.getLogs();
		this.timer = setInterval(() => {
			this.getLogs();
		}, 1000 * 5);
	},
	methods: {
		getLogs() {
			this.$api.sys.getLogs().then(res => {
				let data = res.data.data
				let replaceData = data.replace(/\n(.{8})/gu, '\n');
				this.logData = replaceData.substring(8, replaceData.length - 1);
			})
		},
		onInput(e) {
			if (e == "terminal") {
				this.showTabName = "terminal"
				this.$refs.terminal.active(true)
				this.$refs.logs.active(false)
				this.$messageBus('terminallogs_terminal')
			} else {
				this.showTabName = "logs"
				this.$refs.terminal.active(false)
				this.$refs.logs.active(true)
				this.$messageBus('terminallogs_logs')
			}
		},
		downloadSystemLog() {
			let parameters = {
				token: this.$store.state.access_token
			}
			window.open(`/v2/casaos/health/logs?${qs.stringify(parameters)}`, '_self');
		},
	},
	destroyed() {
		clearInterval(this.timer);
	}
}
</script>

<style lang="scss" scoped>
.cursor-pointer {
	cursor: pointer;
}
</style>
